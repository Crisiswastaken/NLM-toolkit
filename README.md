# NLM-toolkit

A toolkit for organizing, processing, chunking, summarizing, and exporting course materials (especially PDFs and their extracted text) for efficient study and AI-powered summarization.

## Features
- **Course Folder Structure Creation**: Automatically create a standardized folder structure for any course code.
- **PDF Detection**: Scan and monitor course notes folders for PDF files.
- **PDF Text Extraction**: Extract text from PDFs using PyMuPDF.
- **Text Cleaning & Chunking**: Clean and split extracted text into sentence-based, overlapping chunks for downstream processing.
- **AI Summarization**: Generate concise, academic summaries for each chunk using a local Ollama model (model is configurable).
- **Markdown to PDF Export**: Convert markdown summaries to well-formatted PDFs (no pandoc required).
- **Configurable**: All base directories, chunking, and summarization parameters are set in `Tools/config.py` (or via `.env`).
- **Progress Bars**: Uses `tqdm` for progress indication.

## Folder Structure
```
<course-code>/
    <course-code>_notes/         # Place your PDF notes here
    <course-code>_ai_summaries/  # Combined summaries and exported PDFs
    <course-code>_exp_ques/      # Exported expected Q&A PDFs
    <course-code>_md/            # Markdown summaries for each chunk
    <course-code>_html/
    <course-code>_pyqs/
    <course-code>_text/          # Extracted text files from PDFs
    <course-code>_chunks/        # Cleaned and chunked text files
```

## Quickstart Workflow
1. **Create Course Folder Structure**
   ```cmd
   python create_course_folders.py
   ```
   Enter your course code (e.g., `ACP`).
2. **Detect and Monitor PDFs**
   ```cmd
   python find_pdfs_in_notes.py
   ```
   Enter your course code. Optionally, watch for new PDFs in real time.
3. **Extract Text from PDFs**
   ```cmd
   python extract_pdf_text.py
   ```
   Enter your course code. Extracted text files will be saved in `<course-code>_text/`.
4. **Clean and Chunk Text Files**
   ```cmd
   python clean_and_chunk_texts.py
   ```
   Enter your course code. Cleaned and chunked files will be saved in `<course-code>_chunks/`.
5. **Summarize Chunks with Ollama**
   ```cmd
   python summarize_chunks_with_ollama.py
   ```
   Enter your course code. Summaries for each chunk will be saved in `<course-code>_md/`.
6. **Combine Markdown Summaries**
   ```cmd
   python combine_md_files.py
   ```
   Enter your course code. Combined summaries for each file will be saved in the corresponding subfolder of `<course-code>_md/`.
7. **Export Markdown Summaries to PDF**
   ```cmd
   python md_to_pdf.py
   ```
   Enter your course code. PDFs will be saved in `<course-code>_ai_summaries/` and `<course-code>_exp_ques/`.

## Configuration
- Chunk size, overlap, and format are set in `Tools/config.py`.
- Summarization prompt and model are also set in `Tools/config.py`.
- Default: 1200 words per chunk, 200 words overlap, sentence-based splitting, and `llama3` model for summarization.
- You can also set `BASE_DIR` in a `.env` file in the project root.

## Requirements
- Python 3.8+
- See `Tools/requirements.txt` for all Python dependencies.
- Ollama must be installed and running locally for summarization (https://ollama.com/).
- For PDF export, WeasyPrint and its dependencies must be installed (see https://weasyprint.org/ for platform-specific requirements).
- NLTK's `punkt` tokenizer is used for sentence splitting (auto-downloaded if missing).

## Notes
- If you use a virtual environment, activate it before installing requirements.
- Summarization model can be changed in `config.py` without modifying the main script.
- Markdown to PDF conversion uses WeasyPrint and a GitHub-like CSS for formatting.

## License
See `LICENSE` file.
