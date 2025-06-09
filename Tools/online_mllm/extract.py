import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_DOCS_DIR
from general_tools.find_pdfs_in_notes import find_pdf_files
from llama_cloud_services import LlamaExtract
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

# Define a generic schema for text extraction
class PDFText(BaseModel):
    text: str = Field(description="Extracted text content from the PDF")


def extract_text_from_pdfs(course_code):
    notes_dir = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_notes")
    text_dir = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_text")
    os.makedirs(text_dir, exist_ok=True)
    pdf_files = find_pdf_files(course_code)
    if not pdf_files:
        print("No PDF files found to extract.")
        return
    extractor = LlamaExtract()
    # Try to get existing agent, create if not found
    try:
        agent = extractor.get_agent(name="pdf-text-extractor")
    except Exception:
        agent = extractor.create_agent(name="pdf-text-extractor", data_schema=PDFText)
    for pdf_file in pdf_files:
        pdf_path = os.path.join(notes_dir, pdf_file)
        text_path = os.path.join(text_dir, os.path.splitext(pdf_file)[0] + ".txt")
        try:
            result = agent.extract(pdf_path)
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(result.data['text'])
            print(f"Extracted text from {pdf_file} to {text_path}")
        except Exception as e:
            print(f"Failed to extract {pdf_file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        course_code = sys.argv[1].strip()
    else:
        course_code = input("Enter course code: ").strip()
    extract_text_from_pdfs(course_code)
