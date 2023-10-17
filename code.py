import streamlit as st
from dotenv import load_dotenv
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.callbacks import get_openai_callback


load_dotenv('api_key.env')

llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

chat_model = ChatOpenAI()
prompt = "{text} in {language} with input as {inp} and output as {outp}. Give me just the code"

st.title("Code Interpreter")

language = st.sidebar.selectbox("Select a programming language",["C", "C++", "Java", "Python", "C#", "R", "Scala"])
inp = st.sidebar.text_input("Input List (comma-separated)", "1,2,3,4,5")
outp = st.sidebar.text_input("Output List (comma-separated)", "1,3,6,10,15")
text = st.text_input("Text", "give me the sample code for list comprehension")


if st.button("Interpret"):
    chat_prompt = ChatPromptTemplate.from_messages([("system", prompt)])
    p = chat_prompt.format_messages(text=text, language=language, inp=inp, outp=outp)
    out = chat_model(p)
    l=out.content.split('\n')

    st.subheader("Tokens:")
    with get_openai_callback() as cb:
        result = chat_model(p)
        print(st.write(cb))
    st.subheader("Output:")
    print(st.code(out.content))
    ans=out.content

    with open("logs.txt", "a") as logfile:
        logfile.write(f"Language: {language}\n")
        logfile.write(f"Input: {inp}\n")
        logfile.write(f"Output: {outp}\n")
        logfile.write(f"Text: {text}\n")
        logfile.write(f"Code: {ans}\n")
        logfile.write(f"Tokens: {cb}\n")



