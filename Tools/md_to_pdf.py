import os
import markdown
from weasyprint import HTML
from config import BASE_DOCS_DIR
from tqdm import tqdm

def convert_md_to_pdf(course_code):
    md_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_md")
    pdf_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_ai_summaries")
    os.makedirs(pdf_base, exist_ok=True)
    for subfolder in os.listdir(md_base):
        subfolder_path = os.path.join(md_base, subfolder)
        if not os.path.isdir(subfolder_path):
            continue
        for fname in os.listdir(subfolder_path):
            if fname.startswith("summary_") and fname.endswith("_combined.md"):
                md_path = os.path.join(subfolder_path, fname)
                pdf_name = fname.replace(".md", ".pdf")
                pdf_path = os.path.join(pdf_base, pdf_name)
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        md_content = f.read()
                    html_content = markdown.markdown(md_content, extensions=['extra', 'tables', 'fenced_code'])
                    # Add GitHub-like CSS for better formatting
                    html_template = f"""
                    <html>
                    <head>
                        <meta charset='utf-8'>
                        <style>
                        body {{ font-family: 'Segoe UI', 'Arial', sans-serif; margin: 2em; }}
                        h1, h2, h3, h4, h5, h6 {{ font-weight: 600; }}
                        code, pre {{ background: #f6f8fa; border-radius: 6px; padding: 2px 4px; font-size: 95%; }}
                        pre {{ padding: 12px; overflow-x: auto; }}
                        table {{ border-collapse: collapse; }}
                        th, td {{ border: 1px solid #d0d7de; padding: 6px 13px; }}
                        th {{ background: #f6f8fa; }}
                        </style>
                    </head>
                    <body>{html_content}</body>
                    </html>
                    """
                    HTML(string=html_template).write_pdf(pdf_path)
                    print(f"Converted {md_path} to {pdf_path}")
                except Exception as e:
                    print(f"Failed to convert {md_path}: {e}")

if __name__ == "__main__":
    course_code = input("Enter course code: ").strip()
    convert_md_to_pdf(course_code)
