import shutil
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

import config
import speech_to_text
import text_to_speech
import translator

router = APIRouter(prefix="/api")


def save_upload(file: UploadFile, prefix: str) -> Path:
    suffix = Path(file.filename or "").suffix or ".webm"
    path = config.UPLOAD_DIR / f"{prefix}_{uuid.uuid4().hex}{suffix}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return path


def check_lang(lang: str):
    if lang not in config.LANGUAGES:
        raise HTTPException(400, f"Unsupported language: {lang}")


@router.get("/languages")
def languages():
    return config.LANGUAGES


# ---- Day 2: speech to text ----
@router.post("/transcribe")
def transcribe(audio: UploadFile = File(...)):
    path = save_upload(audio, "in")
    text, lang = speech_to_text.transcribe(path)
    return {"text": text, "language": lang}


# ---- Day 3: translation ----
class TranslateRequest(BaseModel):
    text: str
    target_lang: str


@router.post("/translate")
def translate(req: TranslateRequest):
    check_lang(req.target_lang)
    return {"translation": translator.translate(req.text, req.target_lang)}


# ---- Day 4: text to speech ----
class SpeakRequest(BaseModel):
    text: str
    lang: str


@router.post("/speak")
def speak(req: SpeakRequest):
    check_lang(req.lang)
    out = text_to_speech.speak(req.text, req.lang)
    return {"audio_url": f"/output/{out.name}"}


# ---- Day 6: full pipeline (audio in -> translated audio out) ----
@router.post("/voice-translate")
def voice_translate(
    audio: UploadFile = File(...),
    target_lang: str = Form("es"),
    clone_voice: bool = Form(False),
    voice_sample: Optional[UploadFile] = File(None),
):
    check_lang(target_lang)

    input_path = save_upload(audio, "in")
    transcript, detected = speech_to_text.transcribe(input_path)
    if not transcript:
        raise HTTPException(400, "No speech detected in the audio.")

    translation = translator.translate(transcript, target_lang, detected)

    warning = None
    out = None
    if clone_voice:
        try:
            # Use the uploaded sample (best: 6-15 s WAV); otherwise the input audio
            sample = save_upload(voice_sample, "voice") if voice_sample else input_path
            out = text_to_speech.speak(translation, target_lang, speaker_wav=sample)
        except Exception as e:
            warning = f"Voice cloning failed, used a standard voice instead: {e}"
    if out is None:
        out = text_to_speech.speak(translation, target_lang)

    return {
        "transcript": transcript,
        "detected_language": detected,
        "translation": translation,
        "audio_url": f"/output/{out.name}",
        "warning": warning,
    }