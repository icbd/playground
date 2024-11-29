import os

import openai
import streamlit

client = openai.OpenAI(
    base_url=os.environ['OPENAI_BASE_URL'],
    api_key=os.environ['OPENAI_API_KEY'],
)


def chat():
    streamlit.title("Chat Bot")
    if "messages" not in streamlit.session_state:
        streamlit.session_state["messages"] = []

    for message in streamlit.session_state["messages"]:
        with streamlit.chat_message(message['role']):
            streamlit.markdown(message['content'])

    if prompt := streamlit.chat_input("请向我提问:"):
        streamlit.chat_message('user').markdown(prompt)

        streamlit.session_state.messages.append({
            'role': 'user',
            'content': prompt,
        })

        resp = client.chat.completions.create(
            model=os.environ['MODEL_NAME'],
            messages=streamlit.session_state.messages,
            stream=True,
        )

        with streamlit.chat_message('assistant'):
            content = streamlit.write_stream(resp)
            streamlit.session_state.messages.append({
                'role': 'assistant',
                'content': content,
            })


if __name__ == '__main__':
    chat()
