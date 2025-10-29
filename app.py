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
        color: #f7f3e8;            /* Warm off-white */
        border-radius: 4px;
        border: none;
        font-weight: 600; /* Make button text slightly bolder */
    }

    /* Inputs: Add a much stronger border */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {
        background-color: #fdfdfa; /* Soft ivory */
        /* Increase border width and darkness for visibility */
        border: 1.5px solid #a9a9a9; /* A visible mid-gray border */
        border-radius: 4px;
        color: #333333; /* Ensure text typed inside is dark */
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
st.title("📺 YouTube Video Q&A with Gemini")
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
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import google.generativeai as genai

# ----------------------------
# 🌐 PAGE CONFIGURATION
# ----------------------------
st.set_page_config(
    page_title="AskGemini",
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
        color: #3a3a3a; /* CORRECTED: Was #dddddd, now dark for visibility */
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
        color: #f7f3e8;            /* Warm off-white */
        border-radius: 4px;
        border: none;
        font-weight: 600; /* Make button text slightly bolder */
    }

    /* Inputs: Add a much stronger border */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea {
        background-color: #fdfdfa; /* Soft ivory */
        /* Increase border width and darkness for visibility */
        border: 1.5px solid #a9a9a9; /* A visible mid-gray border */
        border-radius: 4px;
        color: #333333; /* Ensure text typed inside is dark */
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

def extract_video_id(url_or_id: str) -> str | None:
    """Extracts the YouTube video ID from a URL or returns the ID if already provided."""
    # Regex for standard watch URL
    watch_match = re.search(r"watch\?v=([a-zA-Z0-9_-]{11})", url_or_id)
    if watch_match:
        return watch_match.group(1)
    
    # Regex for short youtu.be URL
    short_match = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", url_or_id)
    if short_match:
        return short_match.group(1)
    
    # Regex for channel/live URL
    live_match = re.search(r"/live/([a-zA-Z0-9_-]{11})", url_or_id)
    if live_match:
        return live_match.group(1)

    # Check if the input is just the 11-character ID
    if re.fullmatch(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id
        
    return None

def _clean_transcript(text: str) -> str:
    """Helper function to clean transcript text."""
    text = re.sub(r'\[.*?\]', '', text)  # Remove [Music], [Applause]
    text = re.sub(r'>>', '', text)       # Remove ">>"
    text = re.sub(r'\s+', ' ', text)     # Replace multiple spaces with one
    return text.strip()

def get_youtube_transcript(video_id: str) -> str | None:
    """Fetch and clean transcript from YouTube video ID."""
    try:
        # Correct API call
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Correctly access text from each dictionary snippet
        text_snippets = [snippet['text'] for snippet in transcript_list]
        transcript_joined = " ".join(text_snippets)
        
        return _clean_transcript(transcript_joined)

    except (NoTranscriptFound, TranscriptsDisabled):
        st.error(f"Transcript not found or disabled for this video (ID: {video_id}).")
        return None
    except Exception as e:
        st.error(f"Could not retrieve transcript. Error: {e}")
        return None


def get_gemini_answer(transcript: str, question: str) -> str | None:
    """Generate an answer using Gemini API."""
    
    # ---!!! IMPORTANT SECURITY FIX !!!---
    # Load API key from Streamlit secrets, not hardcoded
    api_key = st.secrets.get("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("❌ GOOGLE_API_KEY not set. Please add it to your Streamlit secrets.")
        st.stop() # Stop execution if key is missing

    try:
        genai.configure(api_key=api_key)
        
        # Use a more current model
        model = genai.GenerativeModel("gemini-2.5-flash-latest")

        system_instruction = """
You are a helpful assistant that analyzes YouTube video transcripts. 
Based ONLY on the transcript provided, answer the user's question clearly and concisely.
If the answer cannot be found, state clearly "The transcript does not contain enough information to answer this question."
Do not make assumptions or use external knowledge.
"""

        prompt = f"""
Transcript:
---
{transcript}
---

Question: {question}
"""
        
        response = model.generate_content(
            prompt,
            system_instruction=system_instruction
        )
        return response.text.strip()

    except Exception as e:
        st.error(f"An error occurred while calling the Gemini API: {e}")
        return None


# ----------------------------
#  streamlit APP LOGIC
# ----------------------------
st.title("📺 YouTube Video Q&A with Gemini")
st.markdown("Get answers to your questions directly from YouTube video transcripts using **Gemini AI**!")

# Session state initialization
if 'answer' not in st.session_state:
    st.session_state.answer = ""
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'video_id' not in st.session_state:
    st.session_state.video_id = ""

with st.form("qa_form"):
    video_url_input = st.text_input(
        "🎬 YouTube URL or Video ID",
        help="Paste a full YouTube URL (e.g., youtube.com/watch?v=...) or just the Video ID."
    )
    question_input = st.text_area("💭 Your Question", "Provide a summary of the video.")
    submitted = st.form_submit_button("Analyze Video ✨")

if submitted:
    url_or_id = video_url_input.strip()
    question = question_input.strip()
    
    if not url_or_id:
        st.warning("Please enter a YouTube URL or Video ID.")
    elif not question:
        st.warning("Please enter a question.")
    else:
        # Extract ID from URL/ID input
        video_id = extract_video_id(url_or_id)
        
        if not video_id:
            st.error("Invalid YouTube URL or Video ID. Could not extract ID.")
            st.session_state.answer = ""
            st.session_state.transcript = ""
        else:
            with st.spinner("🔍 Fetching transcript and analyzing..."):
                st.session_state.video_id = video_id
                transcript = get_youtube_transcript(video_id)
                
                if transcript:
                    st.session_state.transcript = transcript
                    answer = get_gemini_answer(transcript, question)
                    if answer:
                        st.session_state.answer = answer
                else:
                    # Error was already shown in get_youtube_transcript
                    st.session_state.answer = ""
                    st.session_state.transcript = ""

# Display results
if st.session_state.answer:
    st.subheader("💡 Gemini’s Answer")
    st.markdown(st.session_state.answer)

if st.session_state.transcript:
    with st.expander("📜 View Full Transcript"):
        st.text_area("", st.session_state.transcript, height=300)

