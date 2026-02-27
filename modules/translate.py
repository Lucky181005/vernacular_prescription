# translation_demo.py

from deep_translator import GoogleTranslator

# Supported Languages
LANGUAGE_MAP = {
    "Hindi": "hi",
    "Telugu": "te"
}

def translate_text(text, language):
    """
    Translates given text into selected language.
    """

    if language not in LANGUAGE_MAP:
        return "Language not supported"

    try:
        translated = GoogleTranslator(
            source="auto",
            target=LANGUAGE_MAP[language]
        ).translate(text)

        return translated

    except Exception as e:
        return f"Translation Error: {str(e)}"


# ------------------ DEMO EXECUTION ------------------

if __name__ == "__main__":

    text = "Take Paracetamol 500 mg twice daily after food."

    print("\nOriginal Text:")
    print(text)

    print("\nTranslated Text:\n")

    print("Telugu:")
    print(translate_text(text, "Telugu"))

    print("\nHindi:")
    print(translate_text(text, "Hindi"))