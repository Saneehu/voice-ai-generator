import time
from deep_translator import GoogleTranslator
import config
import llm

_GOOGLE_CODES = {"zh-cn": "zh-CN"}
_ARGOS_CODES = {"zh-cn": "zh"}


# ---------- Method 1: Google (free, but may block you) ----------
def _google(text, target_lang, source_lang="auto", retries=2):
    code = _GOOGLE_CODES.get(target_lang, target_lang)
    last_error = None
    for attempt in range(retries):
        try:
            return GoogleTranslator(source="auto", target=code).translate(text)
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                time.sleep(2)
    raise last_error


# ---------- Method 2: Argos (offline, downloads a small model once) ----------
def _has_pair(src, tgt):
    import argostranslate.translate as at
    langs = {l.code: l for l in at.get_installed_languages()}
    return (
        src in langs
        and tgt in langs
        and langs[src].get_translation(langs[tgt]) is not None
    )


def _install_pair(src, tgt):
    import argostranslate.package as ap
    ap.update_package_index()
    packages = ap.get_available_packages()
    pkg = next((p for p in packages if p.from_code == src and p.to_code == tgt), None)
    if pkg is None:
        raise RuntimeError(f"No Argos language package for {src} -> {tgt}")
    print(f"Downloading offline translation model {src} -> {tgt} (one time)...")
    ap.install_from_path(pkg.download())


def _argos(text, target_lang, source_lang="auto"):
    import argostranslate.translate as at

    src = "en" if source_lang == "auto" else _ARGOS_CODES.get(source_lang, source_lang)
    tgt = _ARGOS_CODES.get(target_lang, target_lang)
    if src == tgt:
        return text

    # Argos translates through English, so we need X->en and en->Y
    needed = [(src, tgt)] if "en" in (src, tgt) else [(src, "en"), ("en", tgt)]
    for a, b in needed:
        if not _has_pair(a, b):
            _install_pair(a, b)

    return at.translate(text, src, tgt)


# ---------- Method 3: Claude (needs API key) ----------
def _claude(text, target_lang, source_lang="auto"):
    return llm.translate_with_llm(text, config.LANGUAGES.get(target_lang, target_lang))


def translate(text: str, target_lang: str, source_lang: str = "auto") -> str:
    if not text.strip():
        return ""

    has_key = bool(config.ANTHROPIC_API_KEY)
    if config.USE_LLM_TRANSLATION and has_key:
        methods = [_claude, _google, _argos]
    else:
        methods = [_google, _argos] + ([_claude] if has_key else [])

    errors = []
    for method in methods:
        try:
            return method(text, target_lang, source_lang)
        except Exception as e:
            print(f"{method.__name__} failed: {type(e).__name__}: {e}")
            errors.append(f"{method.__name__}: {type(e).__name__}: {e}")

    raise RuntimeError("All translation methods failed. " + " | ".join(errors))