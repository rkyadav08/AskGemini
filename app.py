import streamlit as st
import streamlit as st
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# ----------------------------
# 🌐 PAGE CONFIGURATION
# ----------------------------
st.set_page_config(
    page_title="YouTube Video Q&A",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# 🎨 CUSTOM STYLING
# ----------------------------
st.markdown("""
<style>
    /* "Old Money" Style - High Visibility Modification */

    /* App Background: Keep the warm linen/beige */
    /* Set a default dark text color for high contrast */
    .stApp {
        background-color: #f7f3e8;
        color: #3a3a3a; /* Dark gray-brown for all default text */
    }

    /* Titles, Subheaders, and general markdown text */
    h1, h2, h3, h4, h5, h6,
    .stHeadingContainer p,
    [data-testid="stMarkdown"] p {
        color: #3a3a3a !important; /* Ensure all text is dark */
    }

    /* Labels for inputs */
    label[data-baseweb="form-control-label"] {
        color: #4f4f4f !important; /* A strong, visible label color */
    }

    /* Button: Stays high-contrast (dark bg, light text) */
    .stButton>button {
        background-color: #002147; /* Deep Navy */
        color: #333333;           
        border-radius: 4px;
        border: none;
        font-weight: 600; /* Make button text slightly bolder */
    }

    /* Inputs: Add a much stronger border */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {
        background-color: #303030; /* Soft ivory */
        /* Increase border width and darkness for visibility */
        border: 1.5px solid #a9a9a9; /* A visible mid-gray border */
        border-radius: 4px;
        color: #fffff3; /* Ensure text typed inside is dark */
    }

    /* Placeholder text visibility */
    ::placeholder {
        color: #888888 !important; /* Darker placeholder */
        opacity: 1;
    }

    /* Ensure the red "required" border is also strong */
    .stTextInput[data-testid="stTextInput"] div[data-baseweb="base-input"] > div {
        border-width: 1.5px !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🔧 HELPER FUNCTIONS
# ----------------------------

def get_youtube_transcript(video_id: str):
    """Fetch and clean transcript from YouTube video ID."""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        text = [snippet.text for snippet in transcript]
        transcript_joined = " ".join(text)
        def clean_transcript(text):
            text = re.sub(r'>>', '', text)
            text = re.sub(r'\[.*?\]', '', text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        results = clean_transcript(transcript_joined)
        return results
    except Exception as e:
        st.error(f"Could not retrieve transcript. Error: {e}")
        return None


def get_gemini_answer(transcript: str, question: str):
    """Generate an answer using Gemini API."""
    api_key = "AIzaSyCXo8EuLciVOFwYZZHFuvgkN9XcBU_r6hU"
    if  api_key=="":
        st.error("❌ GOOGLE_API_KEY not set. Please configure your API key.")
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
You are a helpful assistant that analyzes YouTube video transcripts. 
Based ONLY on the transcript below, answer the user's question clearly and concisely.
If the answer cannot be found, say "The transcript does not contain enough information."

Transcript:
---
{transcript}
---

Question: {question}
"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        st.error(f"An error occurred while calling the Gemini API: {e}")
        return None


# ----------------------------
# 🧠 STREAMLIT APP LOGIC
# ----------------------------
st.title("📺 AskGemini")
st.markdown("Get answers to your questions directly from YouTube video transcripts using **Gemini AI**!")

# Session state initialization
if 'answer' not in st.session_state:
    st.session_state.answer = ""
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'video_id' not in st.session_state:
    st.session_state.video_id = ""

with st.form("qa_form"):
    video_id_input = st.text_input(
        "🎬 YouTube Video ID",
        help="Example: For 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', the ID is 'dQw4w9WgXcQ'"
    )
    question_input = st.text_area("💭 Your Question", "Provide a summary of the video.")
    submitted = st.form_submit_button("Analyze Video ✨")

if submitted:
    if not video_id_input.strip():
        st.warning("Please enter a YouTube Video ID.")
    elif not question_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("🔍 Fetching transcript and analyzing..."):
            st.session_state.video_id = video_id_input
            transcript = get_youtube_transcript(video_id_input)
            if transcript:
                st.session_state.transcript = transcript
                answer = get_gemini_answer(transcript, question_input)
                if answer:
                    st.session_state.answer = answer
            else:
                st.session_state.answer = ""
                st.session_state.transcript = ""

# Display results
if st.session_state.answer:
    st.subheader("💡 Gemini’s Answer")
    st.markdown(st.session_state.answer)

if st.session_state.transcript:
    with st.expander("📜 View Full Transcript"):
        st.text_area("", st.session_state.transcript, height=300)




