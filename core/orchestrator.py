# core/orchestrator.py
from agents.script_agent import ScriptAgent
from agents.narrator_agent import NarratorAgent
import os

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

def run_pipeline(raw_script):
    print("🧠 Creator's Studio Agent Pipeline Started...")

    # 1. Refine Script
    print("Refining script...")
    script_agent = ScriptAgent()
    refined_script = script_agent.refine_script(raw_script)
    # Clean up any notes or extra text
    refined_script = refined_script.split('\n')[0].strip()  # Take only the first line
    print(f"Refined: {refined_script}")

    # 2. Generate Narration
    print("Generating narration...")
    narrator_agent = NarratorAgent()
    audio_file_path = narrator_agent.generate_audio(refined_script)
    print(f"Audio generated: {audio_file_path}")

    # 3. Generate Video (Using OpenCV)
    print("Generating video...")
    from agents.video_agent import VideoAgent
    video_agent = VideoAgent()
    video_file_path = video_agent.generate_video(audio_file_path, refined_script)
    print(f"Video generated: {video_file_path}")

    # 4. Mint NFT (Placeholder until Crossmint credentials)
    print("Minting NFT...")
    from agents.publisher_agent import PublisherAgent
    publisher_agent = PublisherAgent()
    mint_id = publisher_agent.mint_asset_nft("email:testuser@example.com:solana", {"script": refined_script})
    print(f"NFT mint ID: {mint_id}")

    return {
        "refined_script": refined_script,
        "audio_path": audio_file_path,
        "video_path": video_file_path,
        "mint_id": mint_id
    }

def main():
    raw_script = input("Paste your raw script: ")
    result = run_pipeline(raw_script)
    print("✅ Pipeline complete!", result)

if __name__ == "__main__":
    main()