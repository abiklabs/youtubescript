import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="YouTube Transcript + Audio Player", layout="centered")

st.title("🎬 YouTube Transcript + Audio Player")
st.markdown(
    "Paste any **public YouTube video URL** below to get the transcript and listen to the audio."
)

def extract_video_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    return match.group(1) if match else None

def fetch_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript

def format_transcript_paragraphs(transcript, max_sentences_per_paragraph=4):
    import re
    paragraphs = []
    sentence_buffer = []

    def ends_with_punct(text):
        return bool(re.search(r'[.!?]$', text.strip()))

    for entry in transcript:
        text = entry['text'].replace('\n', ' ').strip()
        if not text:
            continue
        sentence_buffer.append(text)

        # If buffer is long enough or last sentence ends with punctuation, make paragraph
        if len(sentence_buffer) >= max_sentences_per_paragraph or ends_with_punct(text):
            paragraph = ' '.join(sentence_buffer)
            paragraphs.append(paragraph)
            sentence_buffer = []

    # Add remaining sentences as paragraph
    if sentence_buffer:
        paragraphs.append(' '.join(sentence_buffer))

    return '\n\n'.join(paragraphs)

video_url = st.text_input(
    "🔗 YouTube Video URL", placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)

if st.button("Get Transcript and Play Audio") and video_url:
    with st.spinner("Loading..."):
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("❌ Invalid YouTube URL format.")
        else:
            try:
                transcript = fetch_transcript(video_id)
                formatted_text = format_transcript_paragraphs(transcript)
                st.success("✅ Transcript fetched successfully!")

                # Embed YouTube video player
                youtube_embed_url = f"https://www.youtube.com/embed/{video_id}?controls=1"
                st.markdown(
                    f"""
                    <iframe width="100%" height="120" src="{youtube_embed_url}" 
                    title="YouTube audio player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    """,
                    unsafe_allow_html=True,
                )

                # Display formatted transcript
                st.markdown("### 📝 Transcript")
                st.markdown(formatted_text)

            except Exception as e:
                st.error(f"⚠️ Could not fetch transcript. Reason: {str(e)}")
