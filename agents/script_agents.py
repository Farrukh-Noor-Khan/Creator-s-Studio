# agents/script_agent.py (deep seek)

from mistralai import Mistral
import os
from dotenv import load_dotenv

load_dotenv()  # Load keys from .env

class ScriptAgent:
    def __init__(self):
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model = "mistral-small-latest"  # Good balance of cost/speed

    def refine_script(self, raw_script: str) -> str:
        prompt = f"""
        You are a professional script editor for social media content.
        Refine the following raw script into a concise, engaging, and grammatically correct script suitable for a 30-second YouTube Short or TikTok video.
        Do not add any information not in the original script. Just polish it.

        Raw Script: {raw_script}

        Refined Script:
        """
        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in ScriptAgent: {e}")
            return raw_script  # Fallback: return original script

# Example usage for testing
if __name__ == "__main__":
    agent = ScriptAgent()
    test_script = "hey guys today i wanna talk about why dogs are the best pets they are loyal and fun and cute"
    result = agent.refine_script(test_script)
    print("Refined Script:", result)
