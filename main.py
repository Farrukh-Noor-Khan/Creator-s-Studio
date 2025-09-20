from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents.script_agent import ScriptAgent
from agents.narrator_agent import NarratorAgent
from agents.video_agent import VideoAgent
from agents.publisher_agent import PublisherAgent
import os

app = FastAPI()

# Serve static files from assets/
app.mount("/static", StaticFiles(directory="assets"), name="static")

# Allow CORS for Lovable (adjust if Lovable uses a different port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon; restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScriptRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_content(request: ScriptRequest):
    raw_script = request.text
    if not raw_script:
        raise HTTPException(status_code=400, detail="No script provided")

    try:
        # Refine script
        script_agent = ScriptAgent()
        refined_script = script_agent.refine_script(raw_script)

        # Generate narration
        narrator_agent = NarratorAgent()
        audio_path = narrator_agent.generate_audio(refined_script)
        audio_url = f"/static/{os.path.basename(audio_path)}"

        # Generate video
        video_agent = VideoAgent()
        video_path = video_agent.generate_video(audio_path, refined_script)
        video_url = f"/static/{os.path.basename(video_path)}"

        # Mint NFT (placeholder)
        publisher_agent = PublisherAgent()
        mint_id = publisher_agent.mint_asset_nft("email:testuser@example.com:solana", {"script": refined_script})

        return {
            "message": "Success!",
            "data": {
                "refined_script": refined_script,
                "audio_path": audio_url,
                "video_path": video_url,
                "mint_id": mint_id
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)