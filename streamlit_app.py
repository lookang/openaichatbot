import openai
import streamlit as st

# Prompt Template
prompt_template = """
"Speak like Einstein, a Physics teacher for every question that was asked, 
explain as clearly as possible, assuming the students know very little prior knowledge"
"""

with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "msg_bot" not in st.session_state:
        st.session_state.msg_bot = []

    for message in st.session_state.msg_bot:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    try:

        if prompt := st.chat_input("What is up?"):
            st.session_state.msg_bot.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=[
                                {"role": "system", "content": prompt_template},
                                {"role": "user", "content": prompt},
                            ],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.msg_bot.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(e)
