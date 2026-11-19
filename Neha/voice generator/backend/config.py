import os
from pathlib import Path
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent
load_dotenv(ROOT_DIR / ".env")

UPLOAD_DIR = BACKEND_DIR / "upload"
OUTPUT_DIR = BACKEND_DIR / "output"
FRONTEND_DIR = ROOT_DIR / "Frontend"

for folder in (UPLOAD_DIR, OUTPUT_DIR):
    folder.mkdir(exist_ok=True)

# Whisper model: tiny | base | small | medium  (bigger = more accurate, slower)
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# Optional: use Claude for higher-quality translation
USE_LLM_TRANSLATION = os.getenv("USE_LLM_TRANSLATION", "false").lower() == "true"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")

# code -> display name
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "hi": "Hindi",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "ar": "Arabic",
    "zh-cn": "Chinese",
}