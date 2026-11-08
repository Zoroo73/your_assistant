import streamlit as st
from google import genai
import os

st.title("My AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask something...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6K-KvuwHZqCnUYSEfedj5ZhoRTLMIXaS2fE0BiLsVKEqg"))

            contents = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": m["content"]}]})

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=contents,
                config={
                    "system_instruction": "You are a frank, down-to-earth friend, not a formal assistant. Talk casually like a normal guy chatting with a buddy. Crack jokes often, don't be overly polite or robotic, like say fool sometime only if someone ask you something same for 5 times or extra, and keep things real and relaxed."
                }
            )
            st.write(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})