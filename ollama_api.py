from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM

app = FastAPI()

# Load the Ollama model
llm = OllamaLLM(model="mistral", temperature=0.8)

# Request body for the API
class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_response(query: Query):
    # Generate the response from the model
    prompt = query.question
    response = llm(prompt)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
