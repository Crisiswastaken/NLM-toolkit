import os
from llama_cloud_services import LlamaExtract
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("LLAMA_CLOUD_API_KEY")

if not api_key:
    raise EnvironmentError("LLAMA_CLOUD_API_KEY not found in .env file")

llama = LlamaParse(
    api_key=api_key,
    result_type="text",   # 'text' gives clean plain-text result
    chunk_size=2000,
    chunk_overlap=200,
    split_by="section",   # More semantic than 'page'
    auto_split=True
)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract clean plain-text from a PDF using Llama Cloud.
    Returns the full extracted string.
    """
    documents = llama.load_data(pdf_path)
    return "\n\n".join([doc.text for doc in documents])
