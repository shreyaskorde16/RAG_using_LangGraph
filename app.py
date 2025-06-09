"""
    SREAMLIT APP FOR RAG USING AGENNTIC AI AND LANGGRAPH
    
"""
from generate import get_response
import streamlit as st
import os
import time
#from styles import custom_css_button,custom_css,custom_css3,custom_css_sidebar
import styles
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
tavily_api_key = os.getenv('TAVILY_API_KEY')

st.set_page_config(page_title="My LLM App", layout="wide")

#st.image(os.path.join(os.getcwd(), "static", "llm.png"), width=600)
class handle_status:    
    def __init__(self):
        self.status = False
        
    def get_status(self):
        return self.status
    
    def set_status(self):
        self.status = True
        
    def set_false_status(self):
        self.status=False


# Inject the custom CSS into your Streamlit app
st.markdown(styles.custom_css, unsafe_allow_html=True)
st.markdown(styles.custom_css_button, unsafe_allow_html=True)
st.markdown(styles.custom_css3, unsafe_allow_html=True)
st.markdown(styles.custom_css_sidebar, unsafe_allow_html=True)
st.markdown(styles.css_response, unsafe_allow_html=True)

st.title("🤖 RAG Web application using Agentic AI and LangGraph ")
st.header("Have any Query")
st.subheader("Just ask Anything!")

st.sidebar.title("LLM Configuration")
st.sidebar.write("You can select the LLM model and pass the API key for the selected model.")
with st.sidebar.form(key="My sidebar Form"):
    llm_model = st.selectbox("Select your LLM Model name", ["qwen-qwq-32b", "llama-3.3-70b-versatile","Llama3-70B-8192", "gemma2-9b-it"])
    API_key = st.text_input("Enter your API key")
    
    submit_button = st.form_submit_button("Submit")

form_values = {
    "question": str,
    "answer": str,
}
answer_handler = handle_status()

with st.form(key="My Form"):
    st.title("User Input Form")
    st.subheader("You are Talking with AI 🤖")
    form_values["question"] = st.text_input("Enter your question in brief")   
    
    submit_button = st.form_submit_button("Submit")
    
    if submit_button:

        if not all(form_values.values()):
            st.warning("Please ask the Question")
        else:
            start=time.process_time()
            form_values["answer"], langgraph_output = get_response(form_values["question"],api_key=groq_api_key, tav_key=tavily_api_key)
            st.balloons()
            st.success("Question has been address by AI Bot Successfully!")
            answer_handler.status = True
            st.metric(label="Responnse Time (s)", value=f"{time.process_time() - start}")

with st.container(border=True):
    st.subheader("Response")
    if answer_handler.status:
        st.markdown(form_values["answer"])
        
        
with st.expander("Expand to get more detailed Explanation"):
    if answer_handler.status:
        st.write(langgraph_output[3])
        st.write(langgraph_output[2])
        
    
       
               
    


    
    
