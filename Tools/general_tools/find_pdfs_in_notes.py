import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_DOCS_DIR
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class PDFHandler(FileSystemEventHandler):
    def __init__(self, notes_dir):
        self.notes_dir = notes_dir
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith('.pdf'):
            print(f"New PDF detected: {os.path.basename(event.src_path)}")

def find_pdf_files(course_code):
    notes_dir = os.path.join(BASE_DOCS_DIR, f"{course_code}", f"{course_code}_notes")
    if not os.path.isdir(notes_dir):
        print(f"Directory not found: {notes_dir}")
        return []
    pdf_files = [f for f in os.listdir(notes_dir) if f.lower().endswith('.pdf')]
    return pdf_files

def watch_for_pdfs(course_code):
    notes_dir = os.path.join(BASE_DOCS_DIR, f"{course_code}", f"{course_code}_notes")
    event_handler = PDFHandler(notes_dir)
    observer = Observer()
    observer.schedule(event_handler, notes_dir, recursive=False)
    observer.start()
    print(f"Watching for new PDF files in: {notes_dir}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    course_code = input("Enter course code: ").strip()
    pdfs = find_pdf_files(course_code)
    if pdfs:
        print("PDF files found:")
        for pdf in pdfs:
            print(pdf)
    else:
        print("No PDF files found in the notes directory.")
    watch = input("Do you want to watch for new PDFs? (y/n): ").strip().lower()
    if watch == 'y':
        watch_for_pdfs(course_code)
