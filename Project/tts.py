# tts.py
import tempfile
import os
from gtts import gTTS
import pygame
import pyttsx3
from config import TTS_BACKEND

# Initialize pyttsx3 engine as fallback
_tts_engine = None
if TTS_BACKEND == "pyttsx3":
    _tts_engine = pyttsx3.init()

def speak(text, block=True):
    """
    Speak text. Uses gTTS by default (more natural).
    Falls back to pyttsx3 if configured or gTTS fails.
    """
    if TTS_BACKEND == "pyttsx3":
        _tts_engine.say(text)
        _tts_engine.runAndWait()
        return

    # Use gTTS + pygame
    try:
        t = gTTS(text=text)
        tf = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tf.close()
        t.save(tf.name)

        pygame.mixer.init()
        pygame.mixer.music.load(tf.name)
        pygame.mixer.music.play()
        if block:
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        os.remove(tf.name)
    except Exception as e:
        # fallback to pyttsx3
        if _tts_engine is None:
            _tts_engine = pyttsx3.init()
        _tts_engine.say(text)
        _tts_engine.runAndWait()
