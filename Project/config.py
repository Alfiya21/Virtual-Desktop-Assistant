# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
WAKEWORD = os.getenv("WAKEWORD", "jarvis").lower()
TTS_BACKEND = os.getenv("TTS_BACKEND", "gtts")
MEMORY_FILE = os.getenv("CONVERSATION_MEMORY_FILE", "memory.json")
