# main.py (FastAPI)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ayurvedic Companion API",
    description="API for Ayurvedic wellness chatbot",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Ollama model
try:
    llm = OllamaLLM(
        model="mistral",
        temperature=0.8,
        base_url=os.getenv("OLLAMA_URL", "http://localhost:11434")
    )
except Exception as e:
    logger.error(f"Failed to initialize Ollama: {e}")
    raise

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_response(query: Query):
    try:
        logger.info(f"Received question: {query.question}")
        response = llm(query.question)
        return {"answer": response}
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# For Azure deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)