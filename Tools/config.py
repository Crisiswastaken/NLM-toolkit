import os
from dotenv import load_dotenv

# config.py for create_course_folders.py
# Edit the values below to change base directories or other settings

load_dotenv()
BASE_DOCS_DIR = os.getenv("BASE_DIR")

# Chunking Configuration
CHUNK_SIZE_WORDS = 1200  # 1200–1500 words
CHUNK_SIZE_CHARS = 4500  # ~4500–6000 chars
CHUNK_OVERLAP_WORDS = 200  # 200–300 words
CHUNK_OVERLAP_CHARS = 800  # ~800–1200 chars
CHUNK_FORMAT = "sentence"  # Sentence-based (preferably)
CHUNK_TOKENIZER = "tiktoken"  # or 'llama-cpp-python'
