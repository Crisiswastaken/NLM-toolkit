import os
import tempfile
from datetime import datetime

USER_ANALYSIS_DIR = os.path.join(os.path.dirname(__file__), "user_analysis")
os.makedirs(USER_ANALYSIS_DIR, exist_ok=True)

def record_wrong_answers(wrong_questions, username="default_user"):
    """
    wrong_questions: list of dicts, each with keys like 'question', 'user_answer', 'correct_answer'
    username: optional, for multi-user support
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_file = tempfile.NamedTemporaryFile(
        mode="w", 
        dir=USER_ANALYSIS_DIR, 
        prefix=f"{username}_wrong_{timestamp}_", 
        suffix=".txt", 
        delete=False,
        encoding="utf-8"
    )
    with temp_file as f:
        for idx, q in enumerate(wrong_questions, 1):
            f.write(f"Q{idx}: {q.get('question','')}")
            f.write("\nYour answer: " + str(q.get('user_answer','')))
            f.write("\nCorrect answer: " + str(q.get('correct_answer','')))
            f.write("\n" + ("-" * 40) + "\n")
    print(f"[Watchdog] Wrong answers written to: {temp_file.name}")

# Example usage (to be called from your quiz runner script):
# wrong_questions = [
#     {"question": "What is 2+2?", "user_answer": "5", "correct_answer": "4"},
#     ...
# ]
# record_wrong_answers(wrong_questions, username="vince")
