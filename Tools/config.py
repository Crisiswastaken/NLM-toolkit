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


# Summarization Configuration
SUMMARIZATION_MODEL = "llama3"  # Model name for summarization (used by Ollama)
SUMMARIZATION_PROMPT = """
Summarize the following course content in a concise and academically rigorous way.

- Reduce the length to roughly one-third of the original.
- Include all essential concepts with clear, logical structure.
- Use clean, minimal markdown formatting.
- Focus on clarity, brevity, and information density.
- Omit any commentary, explanations, or output outside the markdown.

The tone must remain professional and academic.
---"""


# Expected Q&A Configuration
EXPECTED_QA_MODEL = "llama3"  # Model name for expected Q&A generation (used by Ollama)

EXPECTED_QA_PROMPT = '''\
From the content below, generate the most likely exam and viva questions.  
For each question, include a concise, accurate answer.  
Format in clean Markdown:  
### Qn. [Question]  
[Answer]

Do not add any intro, summary, or extra comments.

---
''' 


# Quiz Generation Configuration
QUIZ_MODEL = "llama3"  # Model name for quiz generation (used by Ollama)
QUIZ_PROMPT = """
Generate as many multiple choice questions as possible from the text below.
Format strictly as follows:

1. [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Answer: [A/B/C/D]
- Each question must be a single sentence or a short paragraph.
- Each question must have exactly four options (A, B, C, D).
- Only one correct answer per question, marked as 'Answer: X' on a new line after the options.
- Do not include explanations, extra comments, or any text outside this format.
- Do not repeat the question text in the answer line.
- Do not add any intro or summary.
Text:
"""