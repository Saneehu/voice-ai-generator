import uuid
from pathlib import Path
from typing import Optional
from gtts import gTTS
import config

_xtts = None
_GTTS_CODES = {"zh-cn": "zh-CN"}


def _get_xtts():
    """Load the voice-cloning model once (Day 5; first run downloads ~2 GB)."""
    global _xtts
    if _xtts is None:
        import torch
        from TTS.api import TTS
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _xtts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    return _xtts


def speak(text: str, lang: str, speaker_wav: Optional[Path] = None) -> Path:
    """Returns the path of the generated audio file inside output/."""
    if speaker_wav is not None:
        out = config.OUTPUT_DIR / f"{uuid.uuid4().hex}.wav"
        _get_xtts().tts_to_file(
            text=text,
            speaker_wav=str(speaker_wav),
            language=lang,
            file_path=str(out),
        )
        return out

    out = config.OUTPUT_DIR / f"{uuid.uuid4().hex}.mp3"
    gTTS(text=text, lang=_GTTS_CODES.get(lang, lang)).save(str(out))
    return out