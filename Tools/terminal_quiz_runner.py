import os
import re

def parse_quiz_md(quiz_path):
    """Parse quiz markdown file into a list of (question, options, answer) tuples."""
    with open(quiz_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all questions using regex: number dot space, then options, then answer
    pattern = re.compile(
        r'(\d+)\.\s*(.*?)\nA\)\s*(.*?)\nB\)\s*(.*?)\nC\)\s*(.*?)\nD\)\s*(.*?)\nAnswer:\s*([A-D])\)',
        re.DOTALL
    )
    parsed = []
    for match in pattern.finditer(content):
        question_text = match.group(2).strip()
        options = [
            f"A) {match.group(3).strip()}",
            f"B) {match.group(4).strip()}",
            f"C) {match.group(5).strip()}",
            f"D) {match.group(6).strip()}"
        ]
        answer = match.group(7)
        parsed.append((question_text, options, answer))
    return parsed

def run_quiz(quiz_files, username="default_user"):
    score = 0
    total = 0
    wrong_questions = []
    for quiz_file in quiz_files:
        print(f"\n--- Quiz from: {os.path.basename(quiz_file)} ---\n")
        questions = parse_quiz_md(quiz_file)
        for idx, (q, opts, ans) in enumerate(questions, 1):
            print(f"Q{idx}: {q}")
            for o in opts:
                print(f"  {o}")
            user = input("Your answer (A/B/C/D): ").strip().upper()
            if user == ans:
                print("Correct!\n")
                score += 1
            else:
                print(f"Incorrect. Correct answer: {ans}\n")
                wrong_questions.append({
                    'question': q,
                    'user_answer': user,
                    'correct_answer': ans
                })
            total += 1
    print(f"\nQuiz complete! Your score: {score}/{total}")
    if wrong_questions:
        try:
            from quiz_watchdog import record_wrong_answers
            record_wrong_answers(wrong_questions, username=username)
            # Find the latest user analysis file for this user
            import glob
            from quiz_recommender import get_recommendations_from_llm
            user_analysis_dir = os.path.join(os.path.dirname(__file__), "user_analysis")
            pattern = os.path.join(user_analysis_dir, f"{username}_wrong_*.txt")
            files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
            if files:
                get_recommendations_from_llm(files[0])
        except Exception as e:
            print(f"[Watchdog/Recommendation] Error: {e}")

def main():
    course_code = input("Enter course code: ").strip()
    orig_file = input("Enter original file name: ").strip()
    username = input("Enter your username (for analysis): ").strip() or "default_user"
    quiz_dir = os.path.join("..", "Docs", course_code, f"{course_code}_quizzes", orig_file)
    if not os.path.exists(quiz_dir):
        print(f"Quiz directory not found: {quiz_dir}")
        return
    quiz_files = [os.path.join(quiz_dir, f) for f in os.listdir(quiz_dir) if f.endswith('.md')]
    if not quiz_files:
        print("No quiz files found.")
        return
    quiz_files.sort()
    run_quiz(quiz_files, username=username)

if __name__ == "__main__":
    main()
