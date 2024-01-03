from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

# Initializing streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Chatbot with Gemini")

# Initialize session state for chat history if it doesn't exist

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
input = st.text_input("Input:",key="input")
submit = st.button("Ask the question")

#If below given both the consition satisfy then give response
if submit and input:
    response = get_gemini_response(input)
    ## Add user query and response to session chat_history
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The Response is")
    
    # Below for loop will store conversation between bot and user. It will not wait until whole response is generated but it will store simultaneously because in line no. 15 I have written stream=True.
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))
        
st.subheader("The Chat History")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")