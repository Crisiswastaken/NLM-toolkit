import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_DOCS_DIR

def create_course_folders(course_code):
    base_dir = os.path.join(BASE_DOCS_DIR, course_code)
    subfolders = [
        f"{course_code}_notes",
        f"{course_code}_ai_summaries",
        f"{course_code}_exp_ques",
        f"{course_code}_md",
        f"{course_code}_html",
        f"{course_code}_pyqs",
        f"{course_code}_text"
    ]
    os.makedirs(base_dir, exist_ok=True)
    for folder in subfolders:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)
    print(f"Folders created for course: {course_code} in Docs directory")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        course_code = sys.argv[1].strip()
    else:
        course_code = input("Enter course code: ").strip()
    create_course_folders(course_code)