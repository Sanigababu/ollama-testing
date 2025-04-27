from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load the Ollama model
llm = OllamaLLM(model="mistral", temperature=0.8)

# Request body for the API
class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_response(query: Query):
    try:
        # Generate the response from the model
        prompt = query.question
        response = llm(prompt)
        return {"answer": response}
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail="Error processing the request")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Listen on all interfaces