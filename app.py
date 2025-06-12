import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="YouTube Transcript Extractor", layout="centered")

st.title("🎬 YouTube Transcript Extractor")
st.markdown("Paste any **public YouTube video link** below to get the **full transcript** — no timestamps, no fluff.")

def extract_video_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else None

def fetch_clean_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return ' '.join(entry['text'] for entry in transcript)

video_url = st.text_input("🔗 YouTube Video URL", placeholder="e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if st.button("Get Transcript") and video_url:
    with st.spinner("Fetching transcript..."):
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("❌ Invalid YouTube URL format.")
        else:
            try:
                transcript = fetch_clean_transcript(video_id)
                st.success("✅ Transcript fetched successfully!")
                st.text_area("📝 Transcript", transcript, height=400)
            except Exception as e:
                st.error(f"⚠️ Could not fetch transcript. Reason: {str(e)}")
