from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv() # load environment variables from .env file

if not all(
    (
        os.getenv("LANGCHAIN_API_KEY")
        and not os.getenv("LANGCHAIN_API_KEY", "").startswith("REPLACE_"),
        os.getenv("LANGCHAIN_TRACING_V2") == "true",
        os.getenv("LANGSMITH_PROJECT"),
    )
):
    st.warning(
        "LangSmith tracing is not fully configured. Check LANGCHAIN_API_KEY, "
        "LANGCHAIN_TRACING_V2, and LANGSMITH_PROJECT in .env."
    )

# Prompt template for the chatbot
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's queries."),
        ("human", "{question}"),
    ]
)

# Streamlit framework to create the web app
st.title("LangChain Chatbot")
input_text = st.text_input("Ask a question:")


# Model calling using Ollama.
llm = ChatOllama(model="llama3.2")
output_parser = StrOutputParser()
chain = prompt_template | llm | output_parser

if input_text:
    try:
        st.write(chain.invoke({"question": input_text}))
    except Exception as error:
        st.error(
            "Could not reach Ollama. Ensure Ollama is running and the "
            "`llama3.2` model is installed."
        )
        st.exception(error)
