# NLM-toolkit

A toolkit for organizing, processing, and chunking course materials, especially PDFs and their extracted text, for efficient study and AI-powered summarization.

## Features
- **Course Folder Structure Creation**: Automatically create a standardized folder structure for any course code.
- **PDF Detection**: Scan and monitor course notes folders for PDF files.
- **PDF Text Extraction**: Extract text from PDFs using PyMuPDF.
- **Text Cleaning & Chunking**: Clean and split extracted text into sentence-based, overlapping chunks for downstream processing.
- **Configurable**: All base directories and chunking parameters are set in `Tools/config.py` (or via `.env`).
- **Progress Bars**: Uses `tqdm` for progress indication.

## Folder Structure
```
<course-code>/
    <course-code>_notes/         # Place your PDF notes here
    <course-code>_ai_summaries/
    <course-code>_exp_ques/
    <course-code>_md/
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
   - Create a `.env` file in `Tools/` with the following content:
     ```env
     BASE_DIR=C:\Users\vince\OneDrive\Desktop\Private\Programming\Programming Projects\NLM-toolkit\Docs
     ```
   - Or edit `config.py` directly to set `BASE_DOCS_DIR`.

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

## Chunking Configuration
- Chunk size, overlap, and format are set in `config.py`.
- Default: 1200 words per chunk, 200 words overlap, sentence-based splitting.

## Requirements
- Python 3.8+
- See `Tools/requirements.txt` for all Python dependencies.

## Notes
- For sentence-based chunking, NLTK's `punkt` tokenizer is used. The script will auto-download it if missing.
- If you use a virtual environment, activate it before installing requirements.

## License
See `LICENSE` file.
