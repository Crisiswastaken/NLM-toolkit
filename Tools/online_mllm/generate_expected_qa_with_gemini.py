import os
import requests
from tqdm import tqdm
import logging
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_DOCS_DIR, EXPECTED_QA_PROMPT, ONLINE_EXPECTED_QA_MODEL

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/{ONLINE_EXPECTED_QA_MODEL}:generateContent'

def generate_expected_qa(chunk_text):
    prompt = f"""{EXPECTED_QA_PROMPT}\n{chunk_text}\n\n### Questions and Answers:\n"""
    headers = {'Content-Type': 'application/json'}
    params = {'key': GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return None

def process_chunks_for_qa(course_code, chunk_dir, qa_dir):
    chunk_files = [f for f in os.listdir(chunk_dir) if f.lower().endswith('.txt')]
    chunk_files.sort()
    original_file_name = os.path.basename(chunk_dir)
    md_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_md", original_file_name)
    os.makedirs(md_base, exist_ok=True)
    for idx, chunk_file in enumerate(tqdm(chunk_files, desc=f"Q&A for {original_file_name}"), 1):
        chunk_path = os.path.join(chunk_dir, chunk_file)
        with open(chunk_path, 'r', encoding='utf-8') as cf:
            chunk_text = cf.read()
        qa = generate_expected_qa(chunk_text)
        if qa is None:
            logging.error(f"Failed to generate Q&A for {chunk_file}")
            continue
        qa_filename = f"qa_{os.path.splitext(os.path.basename(chunk_file))[0]}.md"
        qa_path = os.path.join(md_base, qa_filename)
        with open(qa_path, 'w', encoding='utf-8') as sf:
            sf.write(qa)
    return len(chunk_files)

def main(course_code=None):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    if course_code is None:
        course_code = input("Enter course code: ").strip()
    chunks_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_chunks")
    if not os.path.exists(chunks_base):
        print(f"Chunks directory does not exist: {chunks_base}")
        return
    chunked_files = [d for d in os.listdir(chunks_base) if os.path.isdir(os.path.join(chunks_base, d))]
    total_files = 0
    total_chunks = 0
    for chunked_file in chunked_files:
        chunk_dir = os.path.join(chunks_base, chunked_file)
        num_chunks = process_chunks_for_qa(course_code, chunk_dir, chunk_dir)
        total_files += 1
        total_chunks += num_chunks
        logging.info(f"{chunked_file}: Q&A generated for {num_chunks} chunks.")
    logging.info(f"\nAll done. {total_files} files processed, {total_chunks} Q&A files generated.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        course_code = sys.argv[1].strip()
        main(course_code)
    else:
        main()
