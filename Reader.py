import os
import re
import csv
from PyPDF2 import PdfReader  # Use PyPDF2 for PDF text extraction

def extract_data_from_text(text):
    """Extract Name, Email, and Phone from the text."""
    name_match = re.search(r"Name:\s*(.*)", text)
    email_match = re.search(r"Email:\s*(.*)", text)
    phone_match = re.search(r"Phone:\s*(.*)", text)

    if name_match and email_match and phone_match:
        phone = phone_match.group(1).strip()
        # Remove "29th November, 2024" from the phone number if it exists
        phone = re.sub(r"29th\sNovember,\s2024", "", phone).strip()

        return {
            "Name": name_match.group(1).strip(),
            "Email": email_match.group(1).strip(),
            "Phone": phone,
        }
    return None

def process_folder(input_folder, output_csv):
    """Process all files in the folder and save extracted data to a CSV."""
    if not os.path.exists(input_folder):
        print(f"Input folder '{input_folder}' does not exist. Exiting.")
        return

    extracted_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(input_folder, filename)
            try:
                # Extract text from PDF
                reader = PdfReader(filepath)
                content = " ".join(page.extract_text() for page in reader.pages)

                # Extract data
                data = extract_data_from_text(content)
                if data:
                    extracted_data.append(data)
                    # Print data to console
                    print(f"Extracted: {data}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if extracted_data:
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Name", "Email", "Phone"])
            writer.writeheader()
            writer.writerows(extracted_data)
        print(f"CSV generated successfully at {output_csv}")
    else:
        print("No data extracted.")

# Input and output paths
input_folder = r"FakePath"
output_csv = r"fake.csv"

process_folder(input_folder, output_csv)
