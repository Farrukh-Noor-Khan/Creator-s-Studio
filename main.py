# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.orchestrator import run_pipeline

app = FastAPI(title="Creator's Studio Agent API")

# Allow Lovable.dev frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon, fine. Restrict in production.
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScriptRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_content(request: ScriptRequest):
    try:
        result = run_pipeline(request.text)
        return {"message": "Success!", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Creator's Studio Agent API is running!"}

# To run: uvicorn main:app --reload --port 8000