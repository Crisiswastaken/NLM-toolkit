import os
from config import BASE_DOCS_DIR
import fitz  # PyMuPDF
from find_pdfs_in_notes import find_pdf_files

# Ensure PyMuPDF is installed
# pip install pymupdf

def extract_text_from_pdfs(course_code):
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
            with fitz.open(pdf_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
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
    extract_text_from_pdfs(course_code)
