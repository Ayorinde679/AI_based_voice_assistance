import speech_recognition as sr
from gtts import gTTS
import os


from groq import Groq
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np









#function to recognize the speech from the saved audio file and convert it to text using google speech recognition api
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    
    # Load the audio file from the recording folder
    recording_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'recording')
    audio_file_path = os.path.join(recording_folder, "output.wav")
    
    try:
        with sr.AudioFile(audio_file_path) as source:
            print("Recognizing speech from saved audio...")
            audio = recognizer.record(source)  # Record the entire audio file
        
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.RequestError:
        print("API unavailable or unresponsive")
        text = ""
    except sr.UnknownValueError:
        print("Unable to recognize speech")
        text = ""
    except FileNotFoundError:
        print("Audio file not found. Please record audio first.")
        text = ""
    
    return text


##for answering questions using groq api
 # Automatically loads from .env in the current directory

api_key = os.environ["GROQ_API_KEY"]



#model to answer questions


def answer_question(text, prompt=None):
    # Sends an optional system prompt to guide the model's behavior.
    
    client = Groq(api_key=api_key)

    default_prompt = "You are a helpful, concise assistant. Answer the user clearly and succinctly, make is short and to point, if text is an empty string, respond with 'No speech was captured. Please check your microphone and try again.'" 


    messages = []
    messages.append({"role": "system", "content": prompt if prompt is not None else default_prompt})
    messages.append({"role": "user", "content": text})

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    result = completion.choices[0].message.content
    return result




#converting text to speech


def text_to_speech(result):
    # Create data folder if it doesn't exist
    data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_folder, exist_ok=True)
    
    # Save the speech in the data folder
    file_path = os.path.join(data_folder, "speech.mp3")
    tts=gTTS(text=result, lang="en")
    tts.save(file_path)
    




