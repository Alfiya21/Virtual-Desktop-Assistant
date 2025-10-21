# wakeword.py
import threading
import time
import sys
from config import WAKEWORD

# Try to import pvporcupine if available
try:
    import pvporcupine
    import pyaudio
    _PORCUPINE_AVAILABLE = True
except Exception:
    _PORCUPINE_AVAILABLE = False

class WakewordListener:
    """
    Provides an interface:
      start(callback_on_wake)
      stop()
    Implementation: tries Porcupine; otherwise the simple SR-based fallback
    """
    def __init__(self, keyword=WAKEWORD):
        self.keyword = keyword.lower()
        self._running = False
        self._thread = None
        self._callback = None

    def start(self, on_wake):
        self._callback = on_wake
        self._running = True
        if _PORCUPINE_AVAILABLE:
            self._thread = threading.Thread(target=self._run_porcupine, daemon=True)
        else:
            self._thread = threading.Thread(target=self._run_fallback, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)

    # Porcupine implementation (better, offline)
    def _run_porcupine(self):
        try:
            porcupine = pvporcupine.create(keywords=[self.keyword])
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )
            while self._running:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm_buf = memoryview(pcm).cast('h')
                result = porcupine.process(pcm_buf)
                if result >= 0:
                    # wake word detected
                    if callable(self._callback):
                        self._callback()
                    # small cooldown
                    time.sleep(0.5)
            audio_stream.stop_stream()
            audio_stream.close()
            pa.terminate()
            porcupine.delete()
        except Exception as e:
            print("Porcupine error, switching to fallback:", e)
            self._run_fallback()

    # Simple fallback: do nothing (main loop will handle on-demand listening)
    # We provide a lightweight polling that does nothing but can be extended.
    def _run_fallback(self):
        # fallback is passive: we rely on active listening in main loop.
        while self._running:
            time.sleep(0.5)
