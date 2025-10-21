# nlp_intent.py
import re
from typing import Tuple, Dict

def classify_intent(text: str) -> Tuple[str, Dict]:
    """
    Return (intent_name, entities)
    Entities: a dict with relevant values (song, site, app, screenshot, etc.)
    Very lightweight rule-based classifier.
    """
    t = text.lower().strip()
    # play <song name>
    m = re.match(r"play (.+)", t)
    if m:
        return "play_music", {"song": m.group(1).strip()}

    # open <website|app>
    m = re.match(r"open (.+)", t)
    if m:
        target = m.group(1).strip()
        # common websites
        if "google" in target:
            return "open_website", {"url": "https://google.com"}
        if "youtube" in target:
            return "open_website", {"url": "https://youtube.com"}
        if "facebook" in target:
            return "open_website", {"url": "https://facebook.com"}
        if target.endswith(".com") or "www." in target:
            return "open_website", {"url": ("https://" + target) if not target.startswith("http") else target}
        # treat as app name
        return "open_app", {"app_name": target}

    # screenshot
    if "screenshot" in t or "take screenshot" in t:
        return "screenshot", {}

    # system status
    if "battery" in t or "cpu" in t or "memory" in t:
        return "system_status", {}

    # news
    if "news" in t:
        return "news", {}

    # fallback: ask AI
    return "ai_fallback", {"query": text}
