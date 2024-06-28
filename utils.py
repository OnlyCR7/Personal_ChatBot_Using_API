import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv
import openai

load_dotenv()  # take environment variables from .env.

openai.api_key = os.getenv('OPENAI_API_KEY')
model = 'gpt-3.5-turbo'

def get_initial_messages():
    messages = [
        {'role': 'system', 'content': 'You are a helpful AI assistant.'},
        {'role': 'user', 'content': 'I want to learn about AI.'},
        {'role': 'assistant', 'content': 'You know about AI... Great! What specifically would you like to learn about?'}
    ]
    return messages

def get_chatgpt_response(messages, model='gpt-3.5-turbo'):
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({'role': role, 'content': content})
    return messages

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
