import json
import os
from modules.extractor import extract_prescription

def main():
    # Define the image path
    image_path = "samples/sample2.jpeg"

    # Check if file exists before processing
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}")
        return

    print(f"Processing prescription: {image_path}...")

    try:
        # Call the extractor
        result = extract_prescription(image_path)

        # Print formatted output
        print("\n--- Structured Data ---")
        print(json.dumps(result["structured_data"], indent=2))
        
        print("\n--- Patient Summary ---")
        print(result["patient_summary"])

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()