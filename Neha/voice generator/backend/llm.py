import anthropic
import config


def translate_with_llm(text: str, target_language_name: str) -> str:
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=config.LLM_MODEL,
        max_tokens=1024,
        system=(
            "You are a professional translator. Translate naturally, keep the "
            "meaning and tone. Output ONLY the translation, nothing else."
        ),
        messages=[
            {"role": "user", "content": f"Translate into {target_language_name}:\n\n{text}"}
        ],
    )
    return message.content[0].text.strip()