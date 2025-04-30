from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
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

# URL for the Ollama model (Azure VM)
OLLAMA_API_URL = os.getenv("OLLAMA_URL", "http://20.246.105.51:11434/api/generate")

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_response(query: Query):
    try:
        logger.info(f"Received question: {query.question}")
        
        # Send the prompt to the Ollama model running on the Azure VM
        response = requests.post(OLLAMA_API_URL, json={"prompt": query.question})
        
        # Check for a successful response
        response.raise_for_status()  # This will raise an error for non-2xx status codes

        # Assuming the Ollama model returns a JSON with a 'response' key
        model_response = response.json()
        answer = model_response.get("response", "No response from model.")

        return {"answer": answer}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with Ollama model: {e}")
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama model: {e}")
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
