import streamlit as st
import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import time

# Set your FastAPI URL
FASTAPI_URL ="https://ollama-testing-fastapi.onrender.com"

# Initialize LLM once
llm = OllamaLLM(model="mistral", temperature=0.8)

def generate_response_from_fastapi(prompt):
    """Send the prompt to FastAPI backend and get the response"""
    response = requests.post(FASTAPI_URL, json={"question": prompt})
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        return "Sorry, there was an issue processing your request. Please try again."

def generate_response(prompt):
    """Generate appropriate response based on user input"""
    normalized_prompt = prompt.lower().strip()
    
    # Casual conversation responses
    if normalized_prompt in ["hi", "hello", "namaste", "hey"]:
        return "Namaste! 🙏 I'm your Ayurvedic companion. How can I support your wellness journey today?"
    
    if normalized_prompt in ["thank you", "thanks"]:
        return "You're most welcome! 🌿 Remember, true health comes from balance - may you find yours today."
    
    if not normalized_prompt:
        return "Please share a wellness question so I can assist you. 🌼"
    
    # Send the prompt to the FastAPI server
    return generate_response_from_fastapi(prompt)

def main():
    st.set_page_config(
        page_title="🌿 Ayurvedic Companion",
        page_icon="🌿",
        layout="centered"
    )
    
    st.title("🌿 Ayurvedic Companion")
    st.caption("A friendly guide to natural wellness")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant", 
            "content": "Namaste! 🙏 I'm your Ayurvedic companion. How can I support your wellness journey today?"
        }]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("Ask about wellness..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking... 🌿"):
                time.sleep(1)  # simulate a natural delay
                response = generate_response(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
