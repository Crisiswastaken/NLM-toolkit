import os
import requests
from tqdm import tqdm
import logging
from config import BASE_DOCS_DIR, QUIZ_MODEL, QUIZ_PROMPT
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')


def generate_quiz(chunk_text):
    prompt = f"{QUIZ_PROMPT}\n{chunk_text}\n\n### Quiz:\n"
    try:
        payload = {
            "model": QUIZ_MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json().get('response', '').strip()
    except Exception as e:
        logging.error(f"Ollama API error: {e}")
        return None


def process_chunks_for_quiz(course_code, chunk_dir):
    chunk_files = [f for f in os.listdir(chunk_dir) if f.lower().endswith('.txt')]
    chunk_files.sort()
    # Store quiz files in the <BASE DIR>/<course code>/<course code>_quizzes/<original file name> directory
    original_file_name = os.path.basename(chunk_dir)
    quiz_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_quizzes", original_file_name)
    os.makedirs(quiz_base, exist_ok=True)
    for idx, chunk_file in enumerate(tqdm(chunk_files, desc=f"Quiz for {original_file_name}"), 1):
        chunk_path = os.path.join(chunk_dir, chunk_file)
        with open(chunk_path, 'r', encoding='utf-8') as cf:
            chunk_text = cf.read()
        quiz = generate_quiz(chunk_text)
        if quiz is None:
            logging.error(f"Failed to generate quiz for {chunk_file}")
            continue
        quiz_filename = f"quiz_{os.path.splitext(os.path.basename(chunk_file))[0]}.md"
        quiz_path = os.path.join(quiz_base, quiz_filename)
        with open(quiz_path, 'w', encoding='utf-8') as sf:
            sf.write(quiz)
    return len(chunk_files)


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
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
        num_chunks = process_chunks_for_quiz(course_code, chunk_dir)
        total_files += 1
        total_chunks += num_chunks
        logging.info(f"{chunked_file}: Quiz generated for {num_chunks} chunks.")
    logging.info(f"\nAll done. {total_files} files processed, {total_chunks} quiz files generated.")


if __name__ == "__main__":
    main()
