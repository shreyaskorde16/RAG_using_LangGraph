## tutorial

import streamlit as st
import os
import pandas as pd

# Define your custom CSS
custom_css = """
<style>
    .stApp {
        background-color: #feffd5;
    }
</style>
"""

custom_css2 = """
<style>
    div.stButton > button:first-child {
        background-color: #0000a0; /* Green background */
        color: white; /* White text */
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        font-weight: bold;
        font-family: Times New Roman, sans-serif;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    div.stButton > button:hover:first-child {
        background-color: #004080; /* Darker green on hover */
    }

    div.stButton > button:focus:not(:active):first-child {
        background-color: #45a21049; /* Darker green when focused */
    }
</style>
"""
custom_css3 = """
<style>
    div.stForm {
        background-color: #cff6ff;
        /*border: 2px solid #121100; /* Blue border */
        border-radius: 10px; /* Rounded corners */  
        padding: 20px; /* Padding inside the form */
    }
    }
</style>
"""

# Inject the custom CSS into your Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(custom_css2, unsafe_allow_html=True)
st.markdown(custom_css3, unsafe_allow_html=True)


st.title("💫 Hello, World!  💫 ")
st.header("Welcome to Streamlit")
st.subheader("This is a simple Streamlit app.")

st.markdown("This is _Markdown_")
pressed1 = st.button("Press me!")
print("First:", pressed1)

pressed2 = st.button("Press me 2!")
print("Second:", pressed2)


st.caption("small caption text")

code_example = """
def green(name):
    print("Hello", name)"""
st.code(code_example, language="python")
st.divider()


st.image(os.path.join(os.getcwd(), "static", "example.jpg"))

st.subheader("Metrics")
st.metric(label="Temperature", value="20 °C", delta="1 °C")
st.metric(label="Humidity", value="50 %", delta="-5 %")


form_values = {
    "Name": None,
    "Feedback": None,
    "Dob": None,
    "Time": None,   
    "Choice": None,
    "Slider Value": None,   
    "Notifications": None,
    "Toggle Value": None,
    "Gender": None
}
# form

with st.form(key="My Form"):
    st.title("User Information Form")
    # Test input
    st.subheader("Text Inputs")
    form_values["Name"] = st.text_input("Enter your name")
    form_values["Feedback"] = st.text_area("Enter your feedback")
    
    # date and time inputs
    st.subheader("Date and Time Inputs")
    form_values["Dob"] = st.date_input("Date of Birth")
    form_values["Time"] = st.time_input("Time of Day")
    
    # selectiors
    
    st.subheader("Selectors")
    
    form_values["Choice"] = st.radio("choose an option", ["Option 1", "Llama3-70B-8192", "Option 3"])
    form_values["Gender"]= st.selectbox("Select your gender", ["qwen-qwq-32b", "Female", "Other"])
    form_values["Slider Value"] = st.select_slider("Select a value",options=["0", "10", "20","30","40","50", "60","70","80","90","100"], value="50")	
    
    # Toggle and checkbox
    st.subheader("Toggle and Checkbox")
    form_values["Notifications"] = st.checkbox("Receive otifications", value=True)
    form_values["Toggle Value"] = st.checkbox("Dark mode?", value=False)
    
    # File upload
    submit_button = st.form_submit_button("Submit")
    if submit_button:
        if not all(form_values.values()):
            st.warning("Please fill in all of the Fileds")
        else:
            st.balloons()
            st.success("Form submitted successfully!")
            st.write("Form Values:")
            for key, value in form_values.items():
                st.write(f"{key}: {value}")
                
                
                
## Session state

if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment Counter"):
    st.session_state.counter += 1
    st.write(f"Counter incremet to : {st.session_state.counter}")
    
if st.button("Reset Counter"):
    st.session_state.counter = 0
    st.write("Counter reset to 0")

st.write("counter value:", st.session_state.counter)
                




























               
                
                
                
                
                
    
    
    
    
    
    
    
    
    
    
    
    