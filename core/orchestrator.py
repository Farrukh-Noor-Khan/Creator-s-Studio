# core/orchestrator.py (Simple Version 1)
from agents.script_agent import ScriptAgent
from agents.narrator_agent import NarratorAgent
import os

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

def main():
    print("🧠 Creator's Studio Agent Pipeline Started...")

    # 1. Get input (later from a file or UI)
    raw_script = input("Paste your raw script: ")

    # 2. Refine Script
    print("Refining script...")
    script_agent = ScriptAgent()
    refined_script = script_agent.refine_script(raw_script)
    print(f"Refined: {refined_script}")

    # 3. Generate Narration
    print("Generating narration...")
    narrator_agent = NarratorAgent()
    audio_file_path = narrator_agent.generate_audio(refined_script)
    print(f"Audio generated: {audio_file_path}")

    print("✅ Pipeline complete!")

if __name__ == "__main__":
    main()
