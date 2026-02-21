import streamlit as st
import base64
import os
from src.helper import recognize_speech_from_mic, answer_question, text_to_speech

# Initialize session state
if 'last_audio_hash' not in st.session_state:
    st.session_state.last_audio_hash = None

st.title("Voice-Driven Question&Answer System for Short-Form Queries🤖") 

st.write("click the record button to ask your question")    


if audio := st.audio_input("Click to record your question"):
    # Create a hash of the audio to detect new recordings
    import hashlib
    audio_hash = hashlib.md5(audio.getbuffer()).hexdigest()
    
    # Only process if it's a new recording
    if audio_hash != st.session_state.last_audio_hash:
        st.session_state.last_audio_hash = audio_hash
        
        # Create recording folder if it doesn't exist
        recording_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recording')
        os.makedirs(recording_folder, exist_ok=True)
        
        # Save the recorded audio
        file_path = os.path.join(recording_folder, "output.wav")
        with open(file_path, "wb") as f:
            f.write(audio.getbuffer())
        
        st.info("🔄 Processing your question...")
        
        # Recognize speech and convert to text
        recognized_text = recognize_speech_from_mic()
        
        if recognized_text:
            st.success("✅ Speech recognized!")
            st.write(f"**You said:** {recognized_text}")
            
            # Get answer from Groq API
            with st.spinner("🤖 Generating answer..."):
                answer = answer_question(recognized_text)
            
            st.write(f"**Answer:** {answer}")
            
            # Convert answer to speech and play it
            with st.spinner("🔊 Generating audio response..."):
                text_to_speech(answer)
            
            # Play the audio response
            with open("data/speech.mp3", "rb") as audio_file:
                audio_bytes = audio_file.read()
            
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
            
            
        else:
            st.warning("⚠️ No speech was captured. Please check your recording and try again.")





