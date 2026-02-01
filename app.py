import os
import streamlit as st
from chatbot.logic import handle_user_query
from chatbot.utils import format_response

st.set_page_config(page_title="Movie Recommendation Chatbot", layout="centered")

st.title("🎥 Movie Recommendation Chatbot (IMDb Open Dataset)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Ask me about movies..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    responses = handle_user_query(user_input)
    bot_reply = format_response(responses)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)