
import time
import webbrowser
import platform
from config import WAKEWORD, OPENAI_API_KEY, NEWSAPI_KEY
from wakeword import WakewordListener
from listener import listen_for_command
from nlp_intent import classify_intent
from automation import open_website, open_app, take_screenshot
from tts import speak
from memory import ConversationMemory
from Jarvis.musiclibrary import music
import requests
import psutil
import openai

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize memory for chat context
memory = ConversationMemory(max_msgs=10)
SYSTEM_PROMPT = "You are Jarvis, a friendly and efficient desktop voice assistant."


#  AI Response Function  

def call_openai_chat(user_text):
    """Send user input + memory to GPT and return response."""
    memory.add_user(user_text)
    messages = memory.get_messages(system_prompt=SYSTEM_PROMPT)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=250,
            temperature=0.6,
        )
        reply = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("OpenAI error:", e)
        reply = "I'm sorry, I couldn't reach my AI service."

    memory.add_assistant(reply)
    return reply


#  Intent Handler Logic  #

def handle_intent(intent, entities):
    """Process recognized intent."""
    if intent == "play_music":
        song = entities.get("song", "").lower()
        url = music.get(song, None)
        if url:
            speak(f"Playing {song}")
            webbrowser.open(url)
        else:
            speak(f"I couldn't find {song}, searching on YouTube.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")

    elif intent == "open_website":
        url = entities.get("url")
        speak("Opening website.")
        open_website(url)

    elif intent == "open_app":
        app_name = entities.get("app_name")
        speak(f"Opening {app_name}.")
        open_app(app_name)

    elif intent == "screenshot":
        path = take_screenshot()
        speak(f"Screenshot saved as {path}")

    elif intent == "system_status":
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        speak(f"CPU usage is {cpu} percent and memory usage is {mem} percent.")

    elif intent == "news":
        if NEWSAPI_KEY:
            try:
                res = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_KEY}")
                if res.status_code == 200:
                    data = res.json()
                    top_articles = data.get("articles", [])[:5]
                    speak("Here are today's top headlines:")
                    for article in top_articles:
                        speak(article["title"])
                else:
                    speak("Unable to fetch news. Let me summarize instead.")
                    summary = call_openai_chat("Summarize today's world news briefly.")
                    speak(summary)
            except Exception as e:
                print(" News API error:", e)
                speak("Something went wrong while fetching the news.")
        else:
            summary = call_openai_chat("Summarize today's world news briefly.")
            speak(summary)

    elif intent == "ai_fallback":
        query = entities.get("query")
        speak("Let me think...")
        answer = call_openai_chat(query)
        speak(answer)

    else:
        speak("I'm not sure how to do that, but I'll check.")
        answer = call_openai_chat(entities.get("query", ""))
        speak(answer)


#  Wake-word Callback Logic  #

def on_wake():
    """Triggered when wake word is detected."""
    speak("Yes?")
    command = listen_for_command(timeout=5, phrase_time_limit=8)

    if not command:
        speak("I didn’t catch that.")
        return

    print(f" Command: {command}")
    intent, entities = classify_intent(command)
    handle_intent(intent, entities)


#  Main Application Loop     #

def run_main_loop():
    """Main entry loop for Jarvis."""
    speak("Initializing Jarvis...")
    print(f" Wake word active: '{WAKEWORD}'")

    listener = WakewordListener()
    listener.start(on_wake)

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nExiting Jarvis...")
        listener.stop()
        speak("Goodbye.")


#  Program Entry Point       

if __name__ == "__main__":
    run_main_loop()
