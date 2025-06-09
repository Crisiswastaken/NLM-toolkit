import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================== GENERAL CONFIG ===============================
# Base directory for all course documents
BASE_DOCS_DIR = os.getenv("BASE_DIR")

# =============================== LLM CONFIGURATION ===============================

# Chunking Configuration
CHUNK_SIZE_WORDS = 1200           # 1200–1500 words
CHUNK_SIZE_CHARS = 4500           # ~4500–6000 chars
CHUNK_OVERLAP_WORDS = 200         # 200–300 words
CHUNK_OVERLAP_CHARS = 800         # ~800–1200 chars
CHUNK_FORMAT = "sentence"         # Sentence-based (preferably)
CHUNK_TOKENIZER = "tiktoken"      # or 'llama-cpp-python'

# Summarization Configuration
LOCAL_SUMMARIZATION_MODEL = "llama3"  # Model name for summarization (Ollama)
ONLINE_SUMMARIZATION_MODEL = "models/gemini-2.0-flash"  # Model name for online summarization (Gemini)
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
LOCAL_EXPECTED_QA_MODEL = "llama3"  # Model name for expected Q&A generation (Ollama)
ONLINE_EXPECTED_QA_MODEL = "models/gemini-2.0-flash"  # Model name for online expected Q&A generation (Gemini)
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
LOCAL_QUIZ_MODEL = "llama3"  # Model name for quiz generation (Ollama)
ONLINE_QUIZ_MODEL = "models/gemini-2.0-flash"  # Model name for online quiz generation (Gemini)
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

# Recommendation prompt for quiz recommender
RECOMMENDATION_MODEL = "llama3"  # Model name for recommendation generation (Ollama)
RECOMMEND_PROMPT = """
You are an expert tutor. The following are questions a user got wrong in a quiz, with their answers and the correct answers. For each question, suggest what topics, concepts, or skills the user should study or practice to improve. Be concise and actionable. List recommendations as bullet points.

{wrong_answers}
"""

# =============================== ONLINE MLLM CONFIGURATION ===============================
# Llama Cloud Extraction API configuration
llama_configuration = {
    "extraction_target": "PER_DOC",
    "extraction_mode": "BALANCED",
    "system_prompt": "",
    "use_reasoning": True,
    "cite_sources": False,
    "chunk_mode": "SECTION",
    "invalidate_cache": False
}

