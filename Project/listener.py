# listener.py
import speech_recognition as sr
from tts import speak

recognizer = sr.Recognizer()

def listen_for_command(timeout=None, phrase_time_limit=None):
    """
    Listens from default microphone and returns recognized text (Google).
    timeout: how long to wait for phrase to start (seconds)
    phrase_time_limit: max length of the phrase (seconds)
    Returns: text or None
    """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return None

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        # network issue
        print("Speech recognition request error:", e)
        speak("I am having trouble reaching the speech service.")
        return None
