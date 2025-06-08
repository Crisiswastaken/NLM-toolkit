import os
import re
from Tools.config import BASE_DOCS_DIR

def combine_md_summaries(course_code):
    md_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_md")
    subfolders = [d for d in os.listdir(md_base) if os.path.isdir(os.path.join(md_base, d))]
    for subfolder in subfolders:
        subfolder_path = os.path.join(md_base, subfolder)
        md_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith('.md')]
        # Group files by base name (excluding chunk number and extension)
        groups = {}
        for md_file in md_files:
            # Match pattern: something_chunk_number.md
            match = re.match(r'(.+)_chunk_\d+\.md$', md_file)
            if match:
                base = match.group(1)
                groups.setdefault(base, []).append(md_file)
        for base, files in groups.items():
            files.sort()  # Ensure order
            combined_content = []
            for md_file in files:
                file_path = os.path.join(subfolder_path, md_file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    combined_content.append(f.read())
            if combined_content:
                combined_path = os.path.join(subfolder_path, f"{base}_combined.md")
                with open(combined_path, 'w', encoding='utf-8') as cf:
                    cf.write('\n\n'.join(combined_content))
                print(f"Combined summary written to {combined_path}")
            else:
                print(f"No .md files found to combine for base '{base}' in {subfolder_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        course_code = sys.argv[1].strip()
    else:
        course_code = input("Enter course code: ").strip()
    combine_md_summaries(course_code)
