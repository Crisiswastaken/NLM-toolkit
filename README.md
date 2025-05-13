# NLM-toolkit

A toolkit for organizing, processing, and chunking course materials, especially PDFs and their extracted text, for efficient study and AI-powered summarization.

## Features
- **Course Folder Structure Creation**: Automatically create a standardized folder structure for any course code.
- **PDF Detection**: Scan and monitor course notes folders for PDF files.
- **PDF Text Extraction**: Extract text from PDFs using PyMuPDF.
- **Text Cleaning & Chunking**: Clean and split extracted text into sentence-based, overlapping chunks for downstream processing.
- **AI Summarization**: Generate concise, academic summaries for each chunk using a local Ollama model (model is configurable).
- **Configurable**: All base directories, chunking, and summarization parameters are set in `Tools/config.py` (or via `.env`).
- **Progress Bars**: Uses `tqdm` for progress indication.

## Folder Structure
```
<course-code>/
    <course-code>_notes/         # Place your PDF notes here
    <course-code>_ai_summaries/  # Combined summaries for each file
    <course-code>_exp_ques/
    <course-code>_md/            # Markdown summaries for each chunk
    <course-code>_html/
    <course-code>_pyqs/
    <course-code>_text/          # Extracted text files from PDFs
    <course-code>_chunks/        # Cleaned and chunked text files
```

## Setup
1. **Clone the repository**
2. **Install dependencies**
   - Open a terminal in the `Tools/` directory and run:
     ```cmd
     pip install -r requirements.txt
     ```
3. **Configure base directory**
   - Create a `.env` file in the project root with the following content:
     ```env
     BASE_DIR=<BASE-DOCS-DIRECTORY>
     ```
   - Or edit `config.py` directly to set `BASE_DOCS_DIR`.
4. **(Optional) Change Summarization Model**
   - In `Tools/config.py`, set `SUMMARIZATION_MODEL` to your preferred Ollama model (e.g., `llama3`, `mistral`, etc.).

## Usage
### 1. Create Course Folder Structure
Run:
```cmd
python create_course_folders.py
```
Enter your course code (e.g., `ACP`).

### 2. Detect and Monitor PDFs
Run:
```cmd
python find_pdfs_in_notes.py
```
Enter your course code. Optionally, watch for new PDFs in real time.

### 3. Extract Text from PDFs
Run:
```cmd
python extract_pdf_text.py
```
Enter your course code. Extracted text files will be saved in `<course-code>_text/`.

### 4. Clean and Chunk Text Files
Run:
```cmd
python clean_and_chunk_texts.py
```
Enter your course code. Cleaned and chunked files will be saved in `<course-code>_chunks/`.

### 5. Summarize Chunks with Ollama
Run:
```cmd
python summarize_chunks_with_ollama.py
```
Enter your course code. Summaries for each chunk will be saved in `<course-code>_md/`, and combined summaries in `<course-code>_ai_summaries/`.

## Chunking & Summarization Configuration
- Chunk size, overlap, and format are set in `config.py`.
- Summarization prompt and model are also set in `config.py`.
- Default: 1200 words per chunk, 200 words overlap, sentence-based splitting, and `llama3` model for summarization.

## Requirements
- Python 3.8+
- See `Tools/requirements.txt` for all Python dependencies.
- Ollama must be installed and running locally for summarization.

## Notes
- For sentence-based chunking, NLTK's `punkt` tokenizer is used. The script will auto-download it if missing.
- If you use a virtual environment, activate it before installing requirements.
- Summarization model can be changed in `config.py` without modifying the main script.

## License
See `LICENSE` file.
