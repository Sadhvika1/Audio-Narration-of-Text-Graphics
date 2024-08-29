Image to Speech Converter
This project is a web application built using Streamlit that converts text from uploaded images into speech. The app is designed to enhance accessibility by enabling users to extract and translate text from images and listen to the converted speech in their preferred language.

Features
Image Upload: Users can upload images in JPG, JPEG, or PNG formats.
Multilingual OCR: EasyOCR is utilized to detect text from images in multiple languages, including English and Hindi.
Text Translation: Integrated with Google Translate API to provide translation of the detected text into over 100 languages.
Text-to-Speech: Uses Google Text-to-Speech (gTTS) to generate speech from the translated text, supporting different languages for audio output.
User-Friendly Interface: The app provides an intuitive interface with a streamlined workflow from image upload to audio playback.
Custom Styling: The app includes visually appealing custom CSS styling for an enhanced user experience.
Installation
To install and run the app locally, follow these steps:

Clone the repository:
bash
Copy code
git clone https://github.com/your-username/image-to-speech-converter.git
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Run the Streamlit application:
streamlit run app.py
Usage
You can just launch the app in your browser.
Upload an image containing text.
Select your preferred output language for speech.
The app will extract the text, translate it, and generate an audio file to listen to.
Tech Stack
Streamlit: Front-end framework for creating web applications.
EasyOCR: Optical Character Recognition (OCR) engine for text detection.
Google Translate API: This is for translating detected text into multiple languages.
gTTS: For converting translated text to speech.
PIL: Python Imaging Library for image processing.
