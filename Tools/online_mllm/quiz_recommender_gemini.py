import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RECOMMEND_PROMPT, RECOMMENDATION_MODEL  # Use the same model as summarization, or set a new one if needed
from generate_quizzes_with_gemini import generate_quiz  # Use the correct function

def get_recommendations_from_gemini(wrong_answers_file):
    with open(wrong_answers_file, 'r', encoding='utf-8') as f:
        wrong_answers = f.read()
    prompt = f"""{RECOMMEND_PROMPT}\n---\n{wrong_answers}\n\n### Recommendations:\n"""
    try:
        # Call Gemini model using the correct function
        recs = generate_quiz(prompt)
        print("\nStudy Recommendations:\n" + recs)
    except Exception as e:
        print(f"[Gemini error] {e}")
        recs = None
    # Delete the file after recommendations
    os.remove(wrong_answers_file)
    print(f"[Info] Deleted analysis file: {wrong_answers_file}")
    return recs

if __name__ == "__main__":
    if len(sys.argv) > 1:
        wrong_answers_file = sys.argv[1]
        get_recommendations_from_gemini(wrong_answers_file)
    else:
        print("Usage: python quiz_recommender_gemini.py <wrong_answers_file>")
