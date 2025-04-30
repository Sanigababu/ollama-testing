import streamlit as st
import time
import requests

FASTAPI_URL = "https://ayushchatbot-ecdqhxg3dtgtefa4.eastus-01.azurewebsites.net/ask"

def generate_local_response(prompt):
    """Call the FastAPI server for a response and ensure Ayurvedic context."""
    try:
        response = requests.post(FASTAPI_URL, json={"question": prompt}, timeout=500)
        response.raise_for_status()
        data = response.json()
        
        answer = data.get("response", "Sorry, I couldn't generate a response.")
        return enrich_with_ayurvedic_wisdom(answer)
    except Exception as e:
        return generate_fallback_response(prompt, error=str(e))

def enrich_with_ayurvedic_wisdom(response):
    """Trim response and add Ayurvedic context in a conversational way."""
    response = response.strip()
    if "vata" in response.lower():
        return "That relates to Vata, which is linked to air and space. To stay balanced, keep warm and avoid cold, dry foods. 🌬️"
    elif "pitta" in response.lower():
        return "Sounds like a Pitta concern. Cooling foods and staying calm help balance the inner fire. 🔥"
    elif "kapha" in response.lower():
        return "That's connected to Kapha — it's steady but can lead to sluggishness. Light food and regular movement are key. 🌱"
    elif "balance" in response.lower():
        return "Ayurveda is all about balance. A calm mind, nourishing food, and daily routine work wonders. 🌿"
    else:
        return response[:200] + "..." if len(response) > 200 else response


def generate_fallback_response(prompt, error=None):
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

    fallback += " Ayurveda teaches us that our health depends on the harmony between mind, body, and spirit. Eat with awareness, sleep well, and nurture your mind through meditation."

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
