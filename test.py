import streamlit as st 
import json 
import os 
import time
from dotenv import load_dotenv
import requests

load_dotenv()
api_token = os.getenv('ASSEMBLY_AI_KEY')

base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": api_token,
    "content-type": "application/json"
}



def assemblyai_stt(url):
    data = {
        "audio_url": url # You can also use a URL to an audio or video file on the web
    }
    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)
    transcript_id = response.json()['id']
    return transcript_id


#Assembly AI LLM Code
transcript_id = "transcript_id"

def post_lemur(transcript_id, query):
    url = "https://api.assemblyai.com/v2/generate/question-answer"    

    questions = [
    {
        "question": query,
        "answer_format": "Short sentence"
    }]

    data = {
        "transcript_ids": [transcript_id],
        "questions": questions
    }

    response = requests.post(url, json=data, headers=headers)
    return response

#Streamlit Code
st.set_page_config(layout="wide", page_title="ChatAudio", page_icon="🔊")

st.title("Chat with Your Audio using LLM")

input_source = st.text_input("Enter the YouTube video URL")

if input_source is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.info("Your uploaded video")
        st.video(input_source)
        transription_id = assemblyai_stt(input_source)
        #st.info(transription_id)
    with col2:
        st.info("Chat Below")
        query = st.text_area("Ask your Query here...")
        if query is not None:
            if st.button("Ask"):
                st.info("Your Query is: " + query)
                lemur_output = post_lemur(transcript_id, query)
                lemur_response = lemur_output.json()
                st.success(lemur_response)


