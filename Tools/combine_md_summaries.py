import os
from config import BASE_DOCS_DIR

def combine_md_summaries(course_code):
    md_base = os.path.join(BASE_DOCS_DIR, course_code, f"{course_code}_md")
    # Output will now be in the same directory as the input (md_base)
    subfolders = [d for d in os.listdir(md_base) if os.path.isdir(os.path.join(md_base, d))]
    for subfolder in subfolders:
        subfolder_path = os.path.join(md_base, subfolder)
        md_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith('.md')]
        md_files.sort()
        combined_content = []
        for md_file in md_files:
            file_path = os.path.join(subfolder_path, md_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                combined_content.append(f.read())
        if combined_content:
            combined_path = os.path.join(subfolder_path, f"summary_{subfolder}_combined.md")
            with open(combined_path, 'w', encoding='utf-8') as cf:
                cf.write('\n\n'.join(combined_content))
            print(f"Combined summary written to {combined_path}")
        else:
            print(f"No .md files found in {subfolder_path}")

if __name__ == "__main__":
    course_code = input("Enter course code: ").strip()
    combine_md_summaries(course_code)
