# memory.py
import json
from collections import deque
from config import MEMORY_FILE

class ConversationMemory:
    def __init__(self, max_msgs=10, filename=MEMORY_FILE):
        self.max_msgs = max_msgs
        self.filename = filename
        self.history = deque(maxlen=max_msgs)
        self._load()

    def add_user(self, text):
        self.history.append({"role": "user", "content": text})
        self._save()

    def add_assistant(self, text):
        self.history.append({"role": "assistant", "content": text})
        self._save()

    def get_messages(self, system_prompt=None):
        msgs = []
        if system_prompt:
            msgs.append({"role":"system", "content": system_prompt})
        msgs.extend(list(self.history))
        return msgs

    def _save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(list(self.history), f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for m in data:
                    self.history.append(m)
        except Exception:
            # no file or parse error -> start fresh
            self.history = deque(maxlen=self.max_msgs)
