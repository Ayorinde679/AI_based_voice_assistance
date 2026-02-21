from setuptools import find_packages, setup

setup(
    name="Voice-Driven Q&A System for Short-Form Queries Using Speech Recognition",
    version="0.0.1",
    author="Ayokunle Ayorinde",
    author_email="ayorindejayokunle@gmail.com",
    packages=find_packages(),
    install_requires=["SpeechRecognition","pipwin","pyaudio","gTTS","google-generativeai","python-dotenv","streamlit"]
)