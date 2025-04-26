import streamlit as st
import PyPDF2
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from gtts import gTTS
import tempfile
import os
import google.generativeai as genai

# Initialize translator
translator = Translator()

# Configure Google Generative AI
GEMINI_API_KEY = "AIzaSyCNMT-XLICWiwxsq2xBHorLO5kY6toRURk"
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    return soup.get_text()

def create_audio(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    audio_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    tts.save(audio_file.name)
    return audio_file.name

def summarize_with_gemini(text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Summarize the following text in a clear manner it cover all content  almost like a given content :\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Gemini API error: {str(e)}")
        return None

# Set page configuration
st.set_page_config(
    page_title="Text Processing & Summarization",
    page_icon="📝",
    layout="wide"
)

# Custom CSS with improved colors and styling
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #f0f2f6;
    }
    .main-header {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(120deg, #2b5876 0%, #4e4376 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    .stButton button {
        background: linear-gradient(120deg, #2b5876 0%, #4e4376 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(43, 88, 118, 0.3);
    }
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        background-color: #ffffff;
        padding: 10px;
    }
    .stSelectbox {
        border-radius: 8px;
    }
    .success-message {
        padding: 1rem;
        border-radius: 12px;
        background-color: #dcfce7;
        border-left: 5px solid #22c55e;
    }
    .error-message {
        padding: 1rem;
        border-radius: 12px;
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
    }
    .output-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(43, 88, 118, 0.1);
    }
    .stInfo {
        background-color: #f0f7ff;
        border: 1px solid #bae6fd;
        color: #0369a1;
        border-radius: 8px;
    }
    .stSuccess {
        background-color: #f0fdf4;
        border: 1px solid #86efac;
        color: #166534;
        border-radius: 8px;
    }
    div[data-testid="stMarkdownContainer"] h3 {
        color: #2b5876;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    div[data-testid="stAudioPlayer"] {
        background: #f8fafc;
        border-radius: 12px;
        padding: 10px;
    }
    div[data-testid="stSpinner"] {
        color: #2b5876;
    }
    </style>
""", unsafe_allow_html=True)

# Update the CSS styling for a more refined dark theme
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #121212;
    }
    .main-header {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        color: #ffffff;
        border-radius: 20px;
        margin: 2rem auto;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(4px);
    }
    
    .output-card {
        background: #1a1a1a;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        backdrop-filter: blur(4px);
    }

    .stButton button {
        background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(255, 255, 255, 0.1);
        background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%);
    }

    .stTextArea textarea {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
    }

    .stInfo, .stSuccess {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 15px;
    }

    div[data-testid="stAudioPlayer"] {
        background: #1a1a1a;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .footer {
        text-align: center;
        padding: 2rem;
        color: #ffffff;
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        border-radius: 20px;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    div[data-testid="stMarkdownContainer"] {
        color: #ffffff;
    }

    .stSelectbox > div {
        background-color: #1a1a1a !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    .stRadio > div {
        background-color: #1a1a1a !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Remove the playback speed CSS rules (delete this entire block)
st.markdown("""
    <style>
    .playback-control {
        background: #1a1a1a;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 10px;
    }

    .playback-label {
        color: #ffffff;
        font-size: 14px;
        margin-bottom: 10px;
        text-align: center;
    }

    div[data-testid="stSlider"] {
        padding: 10px 0;
    }

    .stSlider > div > div > div {
        background-color: #333333 !important;
    }

    .stSlider > div > div > div > div {
        background-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Update the header margin and spacing
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        color: #ffffff;
        border-radius: 20px;
        margin: 0.5rem auto 1.5rem auto;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(4px);
    }

    .output-card {
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        padding: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Update the columns spacing
def main():
    st.markdown("<h1 class='main-header'>🧠 AI Based All in One Text Summarization</h1>", unsafe_allow_html=True)
    
    # Adjust column spacing
    col1, col2 = st.columns([1, 1], gap="small")
    
    with col1:
        st.markdown("""
            <div class='output-card'>
                <h3>📌 Input Settings</h3>
            </div>
        """, unsafe_allow_html=True)
        input_type = st.radio("Select Input Type:", ["Text", "PDF", "URL"], 
                             help="Choose how you want to input your content")
        
        st.markdown("""
            <div class='output-card'>
                <h3>🌍 Language Settings</h3>
            </div>
        """, unsafe_allow_html=True)
        target_lang = st.selectbox(
            "Select Target Language:", 
            ["en", "ta", "hi", "ml", "kn"],
            format_func=lambda x: {
                "en": "🇺🇸 English",
                "ta": "🇮🇳 Tamil",
                "hi": "🇮🇳 Hindi",
                "ml": "🇮🇳 Malayalam",
                "kn": "🇮🇳 Kannada"
            }.get(x, x)
        )

    with col2:
        st.markdown("""
            <div class='output-card'>
                <h3>📄 Content Input</h3>
            </div>
        """, unsafe_allow_html=True)
        text = None

        if input_type == "Text":
            text = st.text_area("Enter your text:", height=250,
                               placeholder="Type or paste your text here...")
        elif input_type == "PDF":
            st.info("📎 Upload your PDF file below")
            uploaded_file = st.file_uploader("", type=['pdf'])
            if uploaded_file:
                with st.spinner("Reading PDF..."):
                    text = extract_text_from_pdf(uploaded_file)
                st.success("PDF successfully loaded!")
        else:  # URL
            url = st.text_input("Enter URL:", placeholder="https://example.com")
            if url:
                with st.spinner("Fetching content..."):
                    text = extract_text_from_url(url)
                st.success("URL content loaded!")

        if st.button("🚀 Process Content", use_container_width=True):
            if not text:
                st.markdown("""
                    <div class='error-message'>
                        Please provide some content to process!
                    </div>
                """, unsafe_allow_html=True)
                return

            with st.spinner("🔄 Processing your content..."):
                # Create result sections without tabs
                summary = summarize_with_gemini(text)
                if summary:
                    st.markdown("<div class='output-card'>", unsafe_allow_html=True)
                    col_sum1, col_sum2 = st.columns(2)
                    
                    with col_sum1:
                        st.markdown("### 📊 Original Summary")
                        st.info(summary)

                    with col_sum2:
                        st.markdown("### 🔄 Translated Version")
                        if target_lang != "en":
                            translated_summary = translator.translate(summary, dest=target_lang).text
                            st.success(translated_summary)
                        else:
                            st.info("Translation not needed (English selected)")
                            translated_summary = summary
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("<div class='output-card'>", unsafe_allow_html=True)
                    st.markdown("### 🎧 Audio Version")
                    # Simplified audio section without speed control
                    audio_path = create_audio(translated_summary, target_lang)
                    st.audio(audio_path)
                    os.unlink(audio_path)
                    st.markdown("</div>", unsafe_allow_html=True)

    # Enhanced footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <h3>MADE BY KARE STUDENTS </h3>
            <p style='font-size: 0.8rem; color: #999;'>© 2025 All in one Summarization</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()