from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents.script_agent import ScriptAgent
from agents.narrator_agent import NarratorAgent
from agents.publisher_agent import PublisherAgent
import os
import logging
import uuid
import json
from pathlib import Path

# Set ImageMagick path correctly
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

# ---------------- Logging Setup ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- FastAPI App ----------------
app = FastAPI(title="Creator's Studio API", version="1.0.0")

# Serve static files from the 'assets' directory
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Enable CORS for all origins (for hackathon demo; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Models ----------------
class ScriptRequest(BaseModel):
    text: str

# ---------------- Routes ----------------
@app.get("/")
async def root():
    return {"message": "Creator's Studio API is running", "status": "OK"}

@app.post("/generate")
async def generate_content(request: Request):
    try:
        # Try to parse the request body
        body = await request.json()
        logger.info(f"Received request body: {body}")
        
        # Check if text field exists
        if "text" not in body:
            raise HTTPException(status_code=422, detail="Missing 'text' field in request")
            
        raw_script = body["text"]
        if not raw_script.strip():
            raise HTTPException(status_code=400, detail="Please provide a non-empty script.")

        logger.info("Starting pipeline for script: %s", raw_script[:50] + "...")

        # 1. Refine the script using Mistral AI
        script_agent = ScriptAgent()
        refined_script = script_agent.refine_script(raw_script)
        logger.info("Script refined successfully.")

        # 2. Generate audio narration using ElevenLabs
        narrator_agent = NarratorAgent()
        audio_path = narrator_agent.generate_audio(refined_script)
        if not audio_path:
            raise HTTPException(status_code=500, detail="Audio generation failed.")
        audio_url = f"/assets/{os.path.basename(audio_path)}"
        logger.info("Audio generated at: %s", audio_path)

        # 3. Generate video with the user's specific content
        video_path = generate_video_with_moviepy(refined_script, audio_path, "final_video")
        video_filename = os.path.basename(video_path)
        video_url = f"/assets/{video_filename}"
        logger.info("Video generated at: %s", video_path)

        # 4. Mint NFT (placeholder or real based on credentials)
        publisher_agent = PublisherAgent()
        mint_id = publisher_agent.mint_asset_nft(
            "email:testuser@example.com:solana", 
            {"script": refined_script}
        )
        logger.info("NFT minting process completed with ID: %s", mint_id)

        return {
            "message": "Success! Your content has been generated.",
            "data": {
                "refined_script": refined_script,
                "audio_url": audio_url,
                "video_url": video_url,
                "mint_id": mint_id
            }
        }
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON received")
        raise HTTPException(status_code=422, detail="Invalid JSON format")
    except Exception as e:
        logger.error("Error in pipeline: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- Video Generation Function ----------------
def generate_video_with_moviepy(script_text, audio_path, output_filename):
    """Generate a simple video with text overlay using moviepy"""
    try:
        from moviepy.editor import TextClip, ColorClip, CompositeVideoClip, AudioFileClip
        
        # Create a unique filename to avoid conflicts
        unique_id = str(uuid.uuid4())[:8]
        output_path = f"assets/{output_filename}_{unique_id}.mp4"
        
        # Create text clip
        txt_clip = TextClip(
            script_text,
            fontsize=40,
            color="white",
            size=(720, 1280),  # Vertical format for social media
            method="caption",
            bg_color="black"
        ).set_duration(10)  # 10 second duration
        
        # Set audio if available
        if os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            txt_clip = txt_clip.set_audio(audio)
            txt_clip = txt_clip.set_duration(audio.duration)
        
        # Write the video file
        txt_clip.write_videofile(
            output_path,
            codec="libx264",
            fps=24,
            verbose=False,
            logger=None
        )
        
        return output_path
        
    except Exception as e:
        logger.error(f"Video generation failed: {str(e)}")
        # Fallback: return a placeholder video path
        return "assets/demo_video.mp4"

@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "Creator's Studio API is running."}

# Create assets directory if it doesn't exist
Path("assets").mkdir(exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)