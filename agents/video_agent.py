# agents/video_agent.py
from moviepy.editor import AudioFileClip, ImageClip, TextClip, CompositeVideoClip
import os

class VideoAgent:
    def __init__(self):
        self.output_dir = "assets"

    def generate_video(self, audio_path: str, script_text: str, output_path: str = "assets/final_video.mp4") -> str:
        try:
            # 1. Load the audio
            audio = AudioFileClip(audio_path)
            duration = audio.duration

            # 2. Create a background (a simple color or image)
            # You can use a static image: background = ImageClip("assets/background.jpg").set_duration(duration)
            background = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=duration) # Black background for 9:16 video

            # 3. Create a text clip with the script
            # MoviePy's TextClip requires ImageMagick on Linux/Mac. On Windows, it can be tricky.
            # This is a potential BLOCKER. Let's find a simpler alternative if this fails.
            txt_clip = TextClip(script_text, fontsize=40, color='white', size=(1000, 800), method='caption').set_duration(duration)
            txt_clip = txt_clip.set_position('center')

            # 4. Composite everything
            video = CompositeVideoClip([background, txt_clip])
            video = video.set_audio(audio)

            # 5. Write the file
            video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
            return output_path

        except Exception as e:
            print(f"❌ Error in VideoAgent: {e}")
            # ULTIMATE FALLBACK: Just return the audio file. The frontend can display it as an audio player.
            return audio_path

# Test
if __name__ == "__main__":
    agent = VideoAgent()
    # You need a test audio file and script
    # agent.generate_video("assets/narration.mp3", "This is a test script text.")
⚠️ If TextClip doesn't install/run: Abandon it. Your demo can show the audio file and the refined script side-by-side in the UI and talk about the video step as the next logical feature. The core agentic workflow is still proven.

Step 2: The Publisher Agent (Web3 Dev)
Create agents/publisher_agent.py. Use Crossmint's API to mint an NFT representing the asset.

python
# agents/publisher_agent.py
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class PublisherAgent:
    def __init__(self):
        self.api_key = os.getenv("CROSSMINT_API_KEY")
        self.project_id = os.getenv("CROSSMINT_PROJECT_ID")
        self.headers = {
            "X-CLIENT-SECRET": self.api_key,
            "X-PROJECT-ID": self.project_id,
            "Content-Type": "application/json"
        }
        self.base_url = "https://staging.crossmint.com/api"

    def mint_asset_nft(self, recipient: str, metadata: dict):
        """Mints an NFT on the Solana Devnet"""
        data = {
            "recipient": recipient, # e.g., "email:yourtestemail@test.com:solana"
            "metadata": {
                "name": "Creator Studio Asset License",
                "image": "https://avatars.githubusercontent.com/u/158211379?s=200&v=4", # Coral logo or a generic image
                "description": "This NFT certifies the ownership of a digital asset created by the Creator's Studio Agent.",
                "attributes": metadata # This is where you put your script hash, video URL, etc.
            },
            "compress": False # For faster minting on devnet
        }
        try:
            response = requests.post(
                f"{self.base_url}/2022-06-09/collections/default/nfts",
                headers=self.headers,
                data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()
            print(f"✅ NFT minted! ID: {result['id']}")
            return result['id']
        except Exception as e:
            print(f"❌ Error minting NFT: {e}")
            return None

# Test
if __name__ == "__main__":
    agent = PublisherAgent()
    test_metadata = {"script": "This is a test script", "date_created": "2025-09-16"}
    agent.mint_asset_nft("email:yourtestemail@test.com:solana", test_metadata)
Step 3: Connect the Frontend (Frontend Dev)
In Lovable.dev, create a simple UI with:

A text area for the raw script input.

A "Generate" button.

A section to display the refined script.

An audio player to play the generated narration.

A link to view the minted NFT.

The frontend will make HTTP POST requests to your Python backend. To enable this, you need to create a simple server. Use FastAPI for this.

Add to requirements.txt:

txt
fastapi
uvicorn
Create main.py in the root:

python
# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.orchestrator import run_pipeline  # You'll need to create this function

app = FastAPI(title="Creator's Studio Agent API")

# Allow Lovable.dev frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For the hackathon, this is fine. In production, restrict this.
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScriptRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_content(request: ScriptRequest):
    try:
        # This function will run the full pipeline and return the paths to the generated assets
        result = run_pipeline(request.text)
        return {"message": "Success!", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Creator's Studio Agent API is running!"}

# To run: uvicorn main:app --reload --port 8000
The Frontend Dev can now point their Lovable.dev project to http://localhost:8000/generate during development.
