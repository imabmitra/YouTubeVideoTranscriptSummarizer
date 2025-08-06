from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
yt_api=YouTubeTranscriptApi()

def get_video_transcript(video_url):      
    video_id=video_url.split("=")[1]
    if("&" in video_id):
        video_id=video_url.split("&")[0]
    
    try:
        transcript_text=yt_api.fetch(video_id,languages=['hi', 'en'])

        transcript = ""
        for i in transcript_text:
            transcript += " " + i.text	
        return transcript

    except:
        try:
            transcript_list = yt_api.list(video_id)
            transcript_text=transcript_list.find_transcript(['hi', 'en'])

            transcript = ""
            for i in transcript_text:
                transcript += " " + i["text"]

            return transcript

        except:

            print("Video does not have transcription")

def get_gemini_response(transcript_txt):
    model=genai.GenerativeModel("gemini-2.0-flash")
    response=model.generate_content(prompt+transcript_txt)
    return response.text

st.header("YouTube Video Transcript Summarizer")    
st.subheader("Powered By- Google Gemini 2.0 Flash")
st.markdown("Creator- Abhishek (https://github.com/imabmitra/)")    
vid_link=st.text_input("Please enter youtube video URL")
language_option = st.selectbox('Select response language',('English', 'Hindi'))
language_limit_option = st.selectbox('Select word limit',('250', '350', '450', '550'))

prompt=f"""You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within {language_limit_option} words. Please provide the summary of the text given here in {language_option}:  """

submit=st.button("Submit")

if vid_link:
    video_id = vid_link.split("=")[1]
    if("&" in video_id):
        video_id=video_id.split("&")[0]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if submit:
    ts_output=get_video_transcript(vid_link)
    if ts_output:
        output= get_gemini_response(ts_output)
        st.markdown("Summery of given Video")
        st.write(output)
    else:
        st.markdown("Not able to fetch video transcript or may be URL is not correct")
