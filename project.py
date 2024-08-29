import streamlit as st
import easyocr
from PIL import Image
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from langdetect import detect, DetectorFactory
import numpy as np
import os

# Fix random seed for langdetect to ensure reproducibility
DetectorFactory.seed = 0

# List of languages supported by EasyOCR (including Hindi and English)
easyocr_languages = [
    'en', 'hi'
]

# Set up the Streamlit app
st.markdown(
    """
    <style>
    .main {
        background-color: #000000;
    }
    .header {
        color: #ff6347;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
    }
    .subheader {
        color: #4682b4;
        text-align: center;
        font-size: 1.5em;
        margin-bottom: 30px;
    }
    .box {
        background-color: #333333;
        color: white;
        border: 2px solid #4682b4;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .play-button {
        background-color: #4caf50;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="header">Image to Speech Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Upload an image and select the output language to get an audio translation of the text in the image.</div>', unsafe_allow_html=True)

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Language selection for output speech
languages = LANGUAGES
output_language = st.selectbox("Select output language", [f"{name.capitalize()} ({code})" for code, name in languages.items()])

def preprocess_image(image):
    # Resize image
    base_width = 1024
    w_percent = (base_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    img = image.resize((base_width, h_size), Image.LANCZOS)
    
    return img

if uploaded_file and output_language:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Preprocess image using the provided preprocessing steps
    preprocessed_image = preprocess_image(image)
    
    # Convert image to array
    preprocessed_image_np = np.array(preprocessed_image)

    # Perform OCR using easyocr
    detected_language = None
    detected_text = ""
    try:
        # Initialize the OCR reader with the appropriate language list
        reader = easyocr.Reader(easyocr_languages, gpu=False)
        result = reader.readtext(preprocessed_image_np)

        # Extract text from result
        detected_text = " ".join([res[1] for res in result])
        
        if not detected_text or not detected_text.strip():
            st.error("No text found in the image.")
        else:
            # Detect language of the detected text
            detected_language = detect(detected_text)
            st.write(f"Detected Text Language: {detected_language}")
    except ValueError as e:
        st.error(f"Error initializing EasyOCR reader: {e}")
        detected_language = None

    if detected_language:
        # Translate text
        st.write("Translating text...")
        translator = Translator()
        lang_code = output_language.split('(')[-1][:-1]
        translated_text = translator.translate(detected_text, src=detected_language, dest=lang_code).text

        st.write("Translated Text:")
        st.markdown(f'<div class="box">{translated_text}</div>', unsafe_allow_html=True)

        # Convert text to speech
        st.write("Generating speech...")
        tts = gTTS(translated_text, lang=lang_code)
        audio_file = "output.mp3"
        tts.save(audio_file)

        # Play audio automatically
        audio_file_path = os.path.abspath(audio_file)
        st.audio(audio_file_path, format='audio/mp3', start_time=0)
