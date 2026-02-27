# import os
# from dotenv import load_dotenv
# from google import genai
# from PIL import Image

# # Load environment variables
# load_dotenv()

# # Get API key
# api_key = os.getenv("GEMINI_API_KEY_TEST")

# if not api_key:
#     raise ValueError("API key not found. Check your .env file.")

# # Create client
# client = genai.Client(api_key=api_key)

# # Load image
# img = Image.open("samples/sample2.jpeg")



# prompt = """
# You are a medical prescription processing AI.

# Analyze the prescription image carefully and extract ALL medicines.

# For EACH medicine extract:

# - medicine_name (exact as written)
# - dosage_pattern (example: 1-0-1 or 2 puffs)
# - frequency (convert OD, BD, TDS only if clearly written)
# - duration
# - food_instruction
# - special_notes
# - confidence_note (High / Medium / Low based on clarity)

# RULES:
# - Do NOT guess missing information.
# - If unclear, write "unclear".
# - Do NOT modify dosage.
# - Do NOT invent medicines.
# - Extract every medicine listed.

# After structured extraction, generate ONE clear patient-friendly summary paragraph:
# - Mention all medicines.
# - Keep dosage exactly the same.
# - Mention timing and duration clearly.
# - Simple English.
# - No medical advice.
# - No extra explanation.

# Return ONLY valid JSON in this format:

# {
#   "structured_data": [
#     {
#       "medicine_name": "",
#       "dosage_pattern": "",
#       "frequency": "",
#       "duration": "",
#       "food_instruction": "",
#       "special_notes": "",
#       "confidence_note": ""
#     }
#   ],
#   "patient_summary": ""
# }
# """

# # Generate response
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=[prompt, img],
#     config={
#         "temperature": 0.1,
#         "max_output_tokens": 4096,
#         "top_k": 40,
#         "top_p": 0.95,
#     }
# )

# print("\nResponse:\n")
# print(response.text)


# modules/extractor.py

import os
import json
from dotenv import load_dotenv
from google import genai
from PIL import Image

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY_TEST")

if not api_key:
    raise ValueError("API key not found. Check your .env file.")

client = genai.Client(api_key=api_key)


PROMPT = """
You are a medical prescription processing AI.

Analyze the prescription image carefully and extract ALL medicines.

For EACH medicine extract:

- medicine_name (exact as written)
- dosage_pattern (example: 1-0-1 or 2 puffs)
- frequency (convert OD, BD, TDS only if clearly written)
- duration
- food_instruction
- special_notes
- confidence_note (High / Medium / Low based on clarity)

RULES:
- Do NOT guess missing information.
- If unclear, write "unclear".
- Do NOT modify dosage.
- Do NOT invent medicines.
- Extract every medicine listed.

After structured extraction, generate ONE clear patient-friendly summary paragraph:
- Mention all medicines.
- Keep dosage exactly the same.
- Mention timing and duration clearly.
- Simple English.
- No medical advice.
- No extra explanation.

Return ONLY valid JSON in this format:

{
  "structured_data": [
    {
      "medicine_name": "",
      "dosage_pattern": "",
      "frequency": "",
      "duration": "",
      "food_instruction": "",
      "special_notes": "",
      "confidence_note": ""
    }
  ],
  "patient_summary": ""
}
"""


def extract_prescription(image_path):
    """
    Takes image path and returns structured JSON + summary.
    """

    img = Image.open(image_path)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[PROMPT, img],
        config={
            "temperature": 0.1,
            "max_output_tokens": 4096,
        }
    )

    raw_text = response.text.strip()

    # Sometimes Gemini wraps output in ```json
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]

    try:
        parsed_json = json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError("Model did not return valid JSON.")

    return parsed_json