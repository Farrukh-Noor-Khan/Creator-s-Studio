# agents/publisher_agent.py
import os
from dotenv import load_dotenv
import json
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
        """Mints an NFT on the Solana Devnet or returns a placeholder if credentials are missing"""
        if not self.api_key or not self.project_id:
            print("⚠️ Crossmint credentials missing. Using placeholder mint ID.")
            return "placeholder_mint_id"  # Placeholder until credentials are added
        else:
            data = {
                "recipient": recipient,  # e.g., "email:yourtestemail@test.com:solana"
                "metadata": {
                    "name": "Creator Studio Asset License",
                    "image": "https://avatars.githubusercontent.com/u/158211379?s=200&v=4",  # Coral logo
                    "description": "This NFT certifies the ownership of a digital asset created by the Creator's Studio Agent.",
                    "attributes": metadata  # e.g., script hash, video URL
                },
                "compress": False  # For faster minting on devnet
            }
            try:
                import requests
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