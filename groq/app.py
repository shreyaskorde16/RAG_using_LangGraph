

from langchain_community.document_loaders import TextLoader
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import create_retrieval_chain
from langchain.schema import Document
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import bs4
import os
import time

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')


st.title("Groq LLM App")
#llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")
llm = Ollama(model="llama2")

prompt =ChatPromptTemplate.from_template("""
    Answer the following question based on the context below.
    Think stept by step and provide a final answer.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.   
    <context>
    {context}
    </context>
    Question: {input}""")





def vector_embedding():
    
    if "vector" not in st.session_state:
        #st.session_state.embeddings= GroqEmbedding(model_name="Llama3-8b-8192")   # data ingestion
        st.session_state.embeddings = OllamaEmbeddings(model="llama2",)
        st.session_state.loader=PyPDFLoader("TajMahal.pdf")
        st.session_state.pdf_document=st.session_state.loader.load()
        st.session_state.page_texts = [doc.page_content for doc in st.session_state.pdf_document]
        st.session_state.documents = [Document(page_content=text) for text in st.session_state.page_texts]
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,)  # chunk creation
        st.session_state.process_pdf = st.session_state.text_splitter.split_documents(st.session_state.documents)
        st.session_state.vector=FAISS.from_documents(documents=st.session_state.process_pdf, embedding=st.session_state.embeddings)


prompt_1 = st.text_input("Enter you Question")

if st.button("Documents Embedding"):
    
    start_embedding=time.process_time()
    vector_embedding()
    st.write(f"Vector Store DB is Ready. Response time: {time.process_time() - start_embedding} seconds")



if prompt_1:
    start=time.process_time()
    document_chain = create_stuff_documents_chain(llm, prompt=prompt)
    retriever = st.session_state.vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": prompt_1})
    print("Responnse time : ", time.process_time() - start)
    st.write("Processing time taken by LLM: ", time.process_time() - start, "seconds")
    st.write(response['answer'])

    with st.expander("Document Similarity Search Results"):
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("----------------------------------------------")








