import os
import requests
from tqdm import tqdm
import logging
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_DOCS_DIR, QUIZ_PROMPT, ONLINE_QUIZ_MODEL

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/{ONLINE_QUIZ_MODEL}:generateContent'

def generate_quiz(chunk_text):
    prompt = f"""{QUIZ_PROMPT}\n{chunk_text}\n\n### Quiz:\n"""
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

def process_chunks_for_quiz(course_code, chunk_dir, quiz_dir):
    chunk_files = [f for f in os.listdir(chunk_dir) if f.lower().endswith('.txt')]
    chunk_files.sort()
    original_file_name = os.path.basename(chunk_dir)
    md_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_md", original_file_name)
    os.makedirs(md_base, exist_ok=True)
    for idx, chunk_file in enumerate(tqdm(chunk_files, desc=f"Quiz for {original_file_name}"), 1):
        chunk_path = os.path.join(chunk_dir, chunk_file)
        with open(chunk_path, 'r', encoding='utf-8') as cf:
            chunk_text = cf.read()
        quiz = generate_quiz(chunk_text)
        if quiz is None:
            logging.error(f"Failed to generate quiz for {chunk_file}")
            continue
        quiz_filename = f"quiz_{os.path.splitext(os.path.basename(chunk_file))[0]}.md"
        quiz_path = os.path.join(md_base, quiz_filename)
        with open(quiz_path, 'w', encoding='utf-8') as sf:
            sf.write(quiz)
    return len(chunk_files)

def generate_general_quiz(course_code, chunks_base):
    """
    Combine all chunk texts from all subfolders in <course_code>_chunks and generate a general quiz.
    """
    all_chunk_texts = []
    for chunked_file in os.listdir(chunks_base):
        chunk_dir = os.path.join(chunks_base, chunked_file)
        if not os.path.isdir(chunk_dir):
            continue
        chunk_files = [f for f in os.listdir(chunk_dir) if f.lower().endswith('.txt')]
        for chunk_file in chunk_files:
            chunk_path = os.path.join(chunk_dir, chunk_file)
            with open(chunk_path, 'r', encoding='utf-8') as cf:
                all_chunk_texts.append(cf.read())
    if not all_chunk_texts:
        logging.warning("No chunk texts found for general quiz.")
        return
    # If the combined text is too large, consider truncating or sampling
    combined_text = '\n\n'.join(all_chunk_texts)
    # Optionally, limit the size to avoid API limits (e.g., 12000 chars)
    max_length = 12000
    if len(combined_text) > max_length:
        combined_text = combined_text[:max_length]
        logging.info(f"Combined chunk text truncated to {max_length} characters for general quiz.")
    general_quiz = generate_quiz(combined_text)
    if general_quiz is None:
        logging.error("Failed to generate general quiz for the course.")
        return
    # Save the general quiz
    md_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_md")
    os.makedirs(md_base, exist_ok=True)
    quiz_path = os.path.join(md_base, "general_quiz.md")
    with open(quiz_path, 'w', encoding='utf-8') as f:
        f.write(general_quiz)
    logging.info(f"General quiz saved to {quiz_path}")

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
        num_chunks = process_chunks_for_quiz(course_code, chunk_dir, chunk_dir)
        total_files += 1
        total_chunks += num_chunks
        logging.info(f"{chunked_file}: Quizzes generated for {num_chunks} chunks.")
    # Generate general quiz for the whole course
    generate_general_quiz(course_code, chunks_base)
    logging.info(f"\nAll done. {total_files} files processed, {total_chunks} quizzes generated.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        course_code = sys.argv[1].strip()
        main(course_code)
    else:
        main()
