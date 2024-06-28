import streamlit as st
from streamlit_chat import message
from utils import get_initial_messages, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
import openai

OPENAI_API_KEY='sk-proj-1IvF9w5N6DmBmGyGIoW9T3BlbkFJZq26bllvxiP3j1WK5xjF'

openai.api_key = os.getenv('OPENAI_API_KEY')
model = 'gpt-3.5-turbo'

st.title("My self AI Chat-Bot...")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Ask : ", key='input')

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_messages()

if query:
    with st.spinner("Thinking..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("All Messages"):
        st.write(st.session_state['messages'])
