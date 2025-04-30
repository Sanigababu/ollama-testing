import streamlit as st
import time
import requests

FASTAPI_URL = "https://ayushchatbot-ecdqhxg3dtgtefa4.eastus-01.azurewebsites.net/ask"

def generate_local_response(prompt):
    """Call the FastAPI server for a response"""
    try:
        response = requests.post(FASTAPI_URL, json={"question": prompt}, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "Sorry, I couldn't generate a response.")
    except Exception as e:
        return generate_fallback_response(prompt, error=str(e))

def generate_fallback_response(prompt, error=None):
    """Fallback response for local logic if API fails"""
    normalized_prompt = prompt.lower().strip()

    if normalized_prompt in ["hi", "hello", "namaste", "hey"]:
        return "Namaste! 🙏 I'm your Ayurvedic companion. How can I support your wellness journey today?"
    
    if normalized_prompt in ["thank you", "thanks"]:
        return "You're most welcome! 🌿 Remember, true health comes from balance - may you find yours today."
    
    if not normalized_prompt:
        return "Please share a wellness question so I can assist you. 🌼"

    fallback = (
        "That's a wonderful question! 🌿 In Ayurveda, each individual is unique, and balance is key. "
    )

    if error:
        fallback += f"\n\n⚠️ *Note: This is a local fallback response due to an error: {error}*"

    return fallback

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
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking... 🌿"):
                time.sleep(1)
                response = generate_local_response(prompt)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
