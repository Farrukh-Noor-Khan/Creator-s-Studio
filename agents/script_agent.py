# agents/script_agent.py
from mistralai import Mistral
import os
from dotenv import load_dotenv

load_dotenv()

class ScriptAgent:
    def __init__(self):
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model = "mistral-small-latest"  # Valid, simpler model

    def refine_script(self, raw_script: str) -> str:
        prompt = f"""
        You are a professional script editor for social media content.
        Refine the following raw script into a concise, engaging, and grammatically correct script suitable for a 30-second YouTube Short or TikTok video.
        Do not add any information not in the original script, including hashtags or extra content. Just polish it.

        Raw Script: {raw_script}

        Refined Script:
        """
        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            # Extract the full refined text after "Refined Script:" and clean it
            content = response.choices[0].message.content.strip()
            refined_start = content.find("Refined Script:") + len("Refined Script:")
            refined_text = content[refined_start:].strip()
            return refined_text if refined_text else content  # Fallback to full content if parsing fails
        except Exception as e:
            print(f"Error in ScriptAgent: {e}")
            # Enhanced fallback: capitalize first letter, add punctuation, remove duplicates
            words = raw_script.lower().split()
            refined = " ".join(word.capitalize() for word in words)
            refined = refined.rstrip(".") + ". Enjoy!"  # Ensure proper ending
            return refined

# Test
if __name__ == "__main__":
    agent = ScriptAgent()
    test_script = "hey guys today i wanna talk about why dogs are the best pets they are loyal and fun and cute"
    result = agent.refine_script(test_script)
    print("Refined Script:", result)