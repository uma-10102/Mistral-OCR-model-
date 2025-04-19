# -*- coding: utf-8 -*-
"""uma 3  (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I-qLdEL5dr-wuyBaO4HSl3bXAYS_KNPn
"""

pip install mistralai

pip install dotenv

pip install pdf2image

!apt-get install poppler-utils

from mistralai import Mistral
from pathlib import Path
import os
import base64
from mistralai import DocumentURLChunk, ImageURLChunk
from mistralai.models import OCRResponse
from dotenv import load_dotenv
from google.colab import userdata
import pdf2image

#Load environment variables
#Load environment variables
#Load environment variables
#Load environment variables
#Load environment variables
#Load environment variables
#Load environment variables
#Load environment variables
from dotenv import load_dotenv
import os
#load_dotenv()
#PDF_PATH = r"C:\\Users\\myhom\\OneDrive\\Documents\\uma research main paper - Copy.pdf"#
MISTRAL_API_KEY = "wgLFxW8uBjxWJC9KOb5dPpcaCQNUqO4K"
#api_key = userdata.get("MISTRAL_API_KEY")

print(MISTRAL_API_KEY)

def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    for img_name, img_path in images_dict.items():
        markdown_str = markdown_str.replace(f"![{img_name}]({img_name})", f"![{img_name}]({img_path})")
    return markdown_str

def save_ocr_results(ocr_response: OCRResponse, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    all_markdowns = []
    for page in ocr_response.pages:
        page_images = {}
        for img in page.images:
            img_data = base64.b64decode(img.image_base64.split(',')[1])
            img_path = os.path.join(images_dir, f"{img.id}.png")
            with open(img_path, 'wb') as f:
                f.write(img_data)
            page_images[img.id] = f"images/{img.id}.png"

    page_markdown = replace_images_in_markdown(page.markdown, page_images)
    all_markdowns.append(page_markdown)

    with open(os.path.join(output_dir, "complete.md"), 'w', encoding='utf-8') as f:
        f.write("\n\n".join(all_markdowns))

def process_pdf() -> None:
    if not MISTRAL_API_KEY:
        raise ValueError("API key is not set. Please configure it in environment variables.")

client = Mistral(api_key=MISTRAL_API_KEY)

# Define PDF file path
PDF_PATH = "/content/98.pdf"

# Convert only the first page of the PDF to an image
image = pdf2image.convert_from_path(PDF_PATH, dpi=500)[0]  # Extract only the first page

# Create output directory
output_dir = f"/content/ocr_results"
os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists without error

# Save the first page image
image_path = os.path.join(output_dir, "page_1.png")
image.save(image_path, "PNG")

# Function to upload and process image
def process_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            uploaded_file = client.files.upload(
                file={
                    "file_name": os.path.basename(image_path),
                    "content": img_file.read(),
                },
                purpose="ocr",
            )

        # Get signed URL
        signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

        # Process the image with OCR
        response = client.ocr.process(
            document=ImageURLChunk(image_url=signed_url.url),
            model="mistral-ocr-latest",
            include_image_base64=True
        )
        return response  # Return successful response

    except Exception as e:
        print(f"OCR processing failed: {e}")
        return None  # Return None if an error occurs

# Process only the first page
result = process_image(image_path)

# Save OCR result if successful
if result:
    save_ocr_results(result, output_dir)  # FIX: Ensuring `os.makedirs` doesn't fail
    print(f"OCR processing complete. Results saved to: {output_dir}")
else:
    print("OCR processing failed for the first page.")

print(result)
