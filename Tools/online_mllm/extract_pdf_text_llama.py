import os
import json
from config import BASE_DOCS_DIR
from find_pdfs_in_notes import find_pdf_files
import requests

# Llama Cloud API endpoint and key (replace with your actual key)
LLAMA_CLOUD_API_URL = "https://api.llama-cloud.com/v1/extract/text"
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY", "YOUR_LLAMA_CLOUD_API_KEY")


def extract_text_llama(pdf_path):
    """Extract text from a PDF using Llama Cloud's extract tool with custom config."""
    llama_config = {
        "extraction_target": "PER_DOC",
        "extraction_mode": "BALANCED",
        "system_prompt": "Extract the text content from this document in a clean, logically ordered, and semantically meaningful way. Ensure:\n- Headings and subheadings are preserved with clear formatting (e.g., \"## Section Title\").\n- Lists, bullet points, and numbering retain structure.\n- Equations or code blocks are retained using markdown formatting if applicable.\n- Tables are flattened into readable text format, with headers and rows clearly separated.\n- Page numbers, footers, and headers are excluded.\n- Remove any watermarks, page artifacts, or boilerplate text.\n- Avoid OCR noise, repeating lines, or metadata.\nThe output should be plain markdown-like text — clean, LLM-friendly, and ready for summarization, question generation, or knowledge extraction.\nOnly return the cleaned content without explanations, metadata, or extra annotations.",
        "use_reasoning": True,
        "cite_sources": False,
        "chunk_mode": "SECTION",
        "invalidate_cache": False
    }
    with open(pdf_path, "rb") as f:
        files = {"file": (os.path.basename(pdf_path), f, "application/pdf")}
        data = {"config": (None, json.dumps(llama_config), "application/json")}
        headers = {"Authorization": f"Bearer {LLAMA_CLOUD_API_KEY}"}
        response = requests.post(LLAMA_CLOUD_API_URL, files=files, data=data, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Llama Cloud extraction failed: {response.status_code} {response.text}")


def extract_text_from_pdfs_llama(course_code):
    notes_dir = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_notes")
    text_dir = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_text")
    os.makedirs(text_dir, exist_ok=True)
    pdf_files = find_pdf_files(course_code)
    if not pdf_files:
        print("No PDF files found to extract.")
        return
    for pdf_file in pdf_files:
        pdf_path = os.path.join(notes_dir, pdf_file)
        text_path = os.path.join(text_dir, os.path.splitext(pdf_file)[0] + ".txt")
        try:
            text = extract_text_llama(pdf_path)
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Extracted text from {pdf_file} to {text_path}")
        except Exception as e:
            print(f"Failed to extract {pdf_file}: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        course_code = sys.argv[1].strip()
    else:
        course_code = input("Enter course code: ").strip()
    extract_text_from_pdfs_llama(course_code)
