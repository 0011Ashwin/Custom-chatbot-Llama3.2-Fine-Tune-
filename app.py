# required packages
from prompt_toolkit import prompt

from langchain_openai import OpenAI # to use OpenAI API
from langchain_openai import ChatOpenAI # to use OpenAI Chat API

from langchain_core.output_parsers import PydanticOutputParser # to parse output into Pydantic models
import streamlit as st # to create the web app
import os # to access environment variables
from dotenv import load_dotenv # to load environment variables from .env file


# load environment variables from .env file
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"]=os.getenv("OPENAI_API_BASE") # Langsmith tracking
os.environ["OPENAI_API_VERSION"]=os.getenv("OPENAI_API_VERSION")


load_dotenv() # load environment variables from .env file
# Prompt template for the chatbot
prompt_template = ChatPromptTemplate.from_template(
    [
        ("system", "You are a helpful assistant. Please response to the user queries."),
        ("user", "Question: {question}"),
    ]
)

# Streamlit framework to create the web app
st.title("LangChain Chatbot")
input_text = st.text_input("Ask a question:")


# openAI LLM 
llm = ChatOpenAI(model = "your model-name")
output_parser = PydanticOutputParser()

chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))

