from pathlib import Path
from faster_whisper import WhisperModel
import config

_model = None


def get_model() -> WhisperModel:
    """Load Whisper once, on first use (first run downloads the model)."""
    global _model
    if _model is None:
        _model = WhisperModel(config.WHISPER_MODEL, device="cpu", compute_type="int8")
    return _model


def transcribe(audio_path: Path):
    """Returns (text, detected_language_code)."""
    segments, info = get_model().transcribe(str(audio_path), beam_size=5)
    text = " ".join(segment.text.strip() for segment in segments).strip()
    return text, info.language