#!/bin/bash
mkdir -p test_audio
cd test_audio

make() {  # make <filename> <voice> <text>
  say -v "$2" -o "$1.wav" --data-format=LEI16@16000 "$3" 2>/dev/null \
    && echo "created $1.wav" \
    || echo "skipped $1 (voice '$2' not installed)"
}

make en_short     "Samantha" "Hello, how are you today?"
make en_long      "Daniel"   "I am building a voice translator. It listens to my speech, converts it to text, translates it into another language, and speaks the result."
make en_numbers   "Samantha" "My phone number is five five five, one two three four, and I live at forty two Main Street."
make es_greeting  "Monica"   "Hola, buenos días. ¿Cómo estás? Me gustaría reservar una mesa para dos personas."
make fr_greeting  "Thomas"   "Bonjour, je voudrais un café et un croissant, s'il vous plaît."
make de_greeting  "Anna"     "Guten Morgen. Wie spät ist es? Ich möchte einen Kaffee bestellen."
make it_greeting  "Alice"    "Buongiorno, vorrei prenotare un tavolo per questa sera."
make hi_greeting  "Lekha"    "नमस्ते, आप कैसे हैं? मैं आपसे मिलकर बहुत खुश हूँ।"
make ja_greeting  "Kyoko"    "こんにちは、お元気ですか。今日はいい天気ですね。"