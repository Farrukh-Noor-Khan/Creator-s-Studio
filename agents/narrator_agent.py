# agents/narrator_agent.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class NarratorAgent:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"  # A default voice (Rachel)
        self.url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"

    def generate_audio(self, text: str, output_path: str = "assets/narration.mp3") -> str:
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
        }
        try:
            response = requests.post(self.url, json=data, headers=headers)
            response.raise_for_status()  # Raises an error for bad status codes

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"Audio saved to {output_path}")
            return output_path
        except Exception as e:
            print(f"Error in NarratorAgent: {e}")
            return None

# Test
if __name__ == "__main__":
    agent = NarratorAgent()
    agent.generate_audio("Hello world! This is a test of our amazing narrator agent.")