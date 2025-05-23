import os
import re
from config import BASE_DOCS_DIR, CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS
from tqdm import tqdm
import nltk
nltk.download('punkt_tab', quiet=True)
from nltk.tokenize import sent_tokenize
from nltk.tokenize import PunktTokenizer


def clean_text(text):
    # Remove extra whitespaces and normalize line breaks
    text = re.sub(r'-\s*\n', '', text)  # Fix hyphenated line breaks
    text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
    text = re.sub(r'[\r\f\v]+', ' ', text)  # Remove special whitespace
    text = text.strip()
    return text

def chunk_sentences(sentences, chunk_size=CHUNK_SIZE_WORDS, overlap=CHUNK_OVERLAP_WORDS):
    chunks = []
    current_chunk = []
    current_len = 0
    i = 0
    while i < len(sentences):
        sent = sentences[i]
        sent_len = len(sent.split())
        if current_len + sent_len <= chunk_size or not current_chunk:
            current_chunk.append(sent)
            current_len += sent_len
            i += 1
        else:
            chunks.append(' '.join(current_chunk))
            # Overlap: go back by overlap words
            overlap_count = 0
            overlap_chunk = []
            j = len(current_chunk) - 1
            while j >= 0 and overlap_count < overlap:
                overlap_chunk.insert(0, current_chunk[j])
                overlap_count += len(current_chunk[j].split())
                j -= 1
            current_chunk = overlap_chunk
            current_len = sum(len(s.split()) for s in current_chunk)
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def process_text_files(course_code):
    input_dir = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_text")
    output_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_chunks")
    os.makedirs(output_base, exist_ok=True)
    txt_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.txt')]
    total_chunks = 0
    for txt_file in tqdm(txt_files, desc="Processing files"):
        file_path = os.path.join(input_dir, txt_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        cleaned = clean_text(raw_text)
        sentences = sent_tokenize(cleaned)
        chunks = chunk_sentences(sentences)
        # Output folder for this file
        file_base = os.path.splitext(txt_file)[0]
        file_out_dir = os.path.join(output_base, file_base)
        os.makedirs(file_out_dir, exist_ok=True)
        for idx, chunk in enumerate(chunks, 1):
            chunk_path = os.path.join(file_out_dir, f"{file_base}_chunk_{idx}.txt")
            with open(chunk_path, 'w', encoding='utf-8') as cf:
                cf.write(chunk)
        print(f"{txt_file}: {len(chunks)} chunks created.")
        total_chunks += len(chunks)
    print(f"\nSummary: {len(txt_files)} files processed, {total_chunks} chunks created.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        course_code = sys.argv[1].strip()
    else:
        course_code = input("Enter course code: ").strip()
    process_text_files(course_code)
