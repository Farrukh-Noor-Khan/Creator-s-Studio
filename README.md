# Creator's Studio 🎬

**Turn Ideas into Videos with AI & Web3 Magic**

Creator's Studio is an AI-powered content creation platform that transforms a simple text prompt into a polished video, complete with professional narration and an NFT certificate of ownership. Built for the **Internet of Agents Hackathon @ Solana Skyline** using **Coral Protocol**.

[![Live Demo](https://img.shields.io/badge/Demo-Live%20App-brightgreen)](http://your-demo-link.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-red)](https://fastapi.tiangolo.com/)

## ✨ Features

- **🤖 Multi-Agent Workflow**: Orchestrated by Coral Protocol for seamless AI agent collaboration.
- **✍️ Script Refinement**: Leverages Mistral AI to turn raw ideas into polished narratives.
- **🎙️ Natural Voiceovers**: Utilizes ElevenLabs for expressive, human-like audio narration.
- **🎬 Automated Video Generation**: Creates social-ready videos with captions using MoviePy.
- **🔗 NFT Certification**: Mints a unique Solana NFT via Crossmint to prove content ownership.
- **⚡ Fast & Efficient**: Goes from idea to final asset in under a minute.

## 🏗️ How It Works

1.  **Input**: User provides a raw text idea (e.g., "A tutorial on baking cookies").
2.  **Processing**:
    - **Script Agent**: Refines the text using Mistral AI.
    - **Narrator Agent**: Generates audio using ElevenLabs.
    - **Video Agent**: Produces a video with MoviePy.
    - **Publisher Agent**: Mints an NFT on Solana via Crossmint.
3.  **Output**: Returns a package containing the refined script, audio file, video file, and NFT mint ID.

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Agent Orchestration** | Coral Protocol |
| **Backend API** | FastAPI (Python) |
| **Text AI** | Mistral AI |
| **Voice AI** | ElevenLabs |
| **Video Generation** | MoviePy, ImageMagick |
| **Blockchain** | Solana, Crossmint API |
| **Frontend** | React, Tailwind CSS,  (Loveable) |

## 📦 Installation & Setup

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.10+
- ImageMagick (for video generation)
- FFmpeg
- API keys for Mistral AI, ElevenLabs, and Crossmint.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/creators-studio.git
cd creators-studio
```

2. Create a Virtual Environment and Install Dependencies

```bash
# Create a virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate
# Or (Mac/Linux)
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

3. Environment Configuration

Create a .env file in the root directory and add your API keys:

```ini
MISTRAL_API_KEY=your_mistral_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
CROSSMINT_API_KEY=your_crossmint_key_here
CROSSMINT_PROJECT_ID=your_crossmint_project_id_here

# Optional: Set ImageMagick binary path if not in system PATH
IMAGEMAGICK_BINARY=C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe
```

4. Run the Backend Server

```bash
uvicorn main:app --reload --port ....
```

The API will be available at http://localhost..... Visit http://localhost: for the interactive Swagger/OpenAPI documentation.

🚀 Usage

1. Using the API

Send a POST request to the /generate endpoint:

```bash
curl -X POST "http://localhost:..../generate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your raw idea goes here"}'
```

2. Example Response

```json
{
  "message": "Success!",
  "data": {
    "refined_script": "Your polished script...",
    "audio_url": "/assets/narration_abc123.mp3",
    "video_url": "/assets/final_video_xyz789.mp4",
    "mint_id": "placeholder_mint_id_or_solana_tx_id"
  }
}
```

📁 Project Structure

```
creators-studio/
├── agents/                 # AI Agent Modules
│   ├── script_agent.py     # Mistral AI integration
│   ├── narrator_agent.py   # ElevenLabs integration
│   ├── video_agent.py      # MoviePy video generation
│   └── publisher_agent.py  # Crossmint NFT minting
├── assets/                 # Generated audio/video files
├── core/
│   └── orchestrator.py     # Main workflow logic
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (gitignored)
└── README.md
```

🌟 API Reference

POST /generate

Generates content from a text prompt.

Request Body:

```json
{
  "text": "string"
}
```

Response:

· 200 OK: Returns JSON with URLs to generated assets.
· 422 Unprocessable Entity: Invalid input.
· 500 Internal Server Error: Processing error.

🤝 Contributing

We welcome contributions! Please feel free to submit issues, fork the repository, and create pull requests.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

· Coral Protocol for the agent orchestration framework.
· Solana and Crossmint for the blockchain infrastructure.
· Mistral AI and ElevenLabs for their powerful AI models.
· Lablab.ai and the hackathon organizers for the incredible opportunity.

---

Built with ❤️ for the Internet of Agents Hackathon @ Solana Skyline.

```

### **To use this README:**

1.  Copy the entire text above.
2.  Create a new file in your project's root folder named `README.md`.
3.  Paste the content.
4.  **Crucially, replace the placeholder text:**
    *   `[![Live Demo](...)](http://your-demo-link.com)` - Replace with your actual demo link (if you have one deployed).
    *   `git clone https://github.com/your-username/creators-studio.git` - Replace with your actual GitHub repository URL.
    *   Add your team members' names and GitHub profiles in the **Team** section.
5.  Commit and push this file to your GitHub repository.

This README will serve as a perfect landing page for your project, making it look professional and well-documented.# Creators Studio Agent
