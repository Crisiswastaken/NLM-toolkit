import os
import subprocess
from tqdm import tqdm
import logging
from config import BASE_DOCS_DIR, SUMMARIZATION_PROMPT, SUMMARIZATION_MODEL


def summarize_chunk(chunk_text):
    prompt = f""" {SUMMARIZATION_PROMPT}
---
{chunk_text}

### Summary:
"""
    try:
        result = subprocess.run(
            ["ollama", "run", SUMMARIZATION_MODEL],
            input=prompt.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120
        )
        if result.returncode != 0:
            logging.error(f"Ollama error: {result.stderr.decode('utf-8')}")
            return None
        return result.stdout.decode('utf-8').strip()
    except Exception as e:
        logging.error(f"Subprocess error: {e}")
        return None

def process_chunks(course_code, chunk_dir, md_dir, summary_dir):
    chunk_files = [f for f in os.listdir(chunk_dir) if f.lower().endswith('.txt')]
    chunk_files.sort()
    summaries = []
    os.makedirs(md_dir, exist_ok=True)
    for idx, chunk_file in enumerate(tqdm(chunk_files, desc=f"Summarizing {os.path.basename(chunk_dir)}"), 1):
        chunk_path = os.path.join(chunk_dir, chunk_file)
        with open(chunk_path, 'r', encoding='utf-8') as cf:
            chunk_text = cf.read()
        summary = summarize_chunk(chunk_text)
        if summary is None:
            logging.error(f"Failed to summarize {chunk_file}")
            continue
        summary_filename = f"summary_{os.path.splitext(os.path.basename(chunk_file))[0]}.md"
        summary_path = os.path.join(md_dir, summary_filename)
        with open(summary_path, 'w', encoding='utf-8') as sf:
            sf.write(summary)
        summaries.append(summary)
    return len(chunk_files), len(summaries)

def main(course_code=None):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    if course_code is None:
        course_code = input("Enter course code: ").strip()
    chunks_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_chunks")
    md_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_md")
    summary_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_ai_summaries")
    os.makedirs(md_base, exist_ok=True)
    os.makedirs(summary_base, exist_ok=True)
    chunked_files = [d for d in os.listdir(chunks_base) if os.path.isdir(os.path.join(chunks_base, d))]
    total_files = 0
    total_chunks = 0
    for chunked_file in chunked_files:
        chunk_dir = os.path.join(chunks_base, chunked_file)
        md_dir = os.path.join(md_base, chunked_file)
        num_chunks, num_summaries = process_chunks(course_code, chunk_dir, md_dir, summary_base)
        total_files += 1
        total_chunks += num_summaries
        logging.info(f"{chunked_file}: {num_summaries} summaries generated from {num_chunks} chunks.")
    logging.info(f"\nAll done. {total_files} files processed, {total_chunks} chunk summaries generated.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        course_code = sys.argv[1].strip()
        main(course_code)
    else:
        main()
