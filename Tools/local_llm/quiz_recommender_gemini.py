import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'online_mllm')))
from config import RECOMMEND_PROMPT, RECOMMENDATION_MODEL  # Use the same model as summarization, or set a new one if needed
import importlib
import importlib.util

def get_recommendations_from_gemini(wrong_answers_file):
    with open(wrong_answers_file, 'r', encoding='utf-8') as f:
        wrong_answers = f.read()
    prompt = f"""{RECOMMEND_PROMPT}\n---\n{wrong_answers}\n\n### Recommendations:\n"""
    try:
        # Dynamically import the Gemini quiz generator from the correct path
        gemini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'online_mllm', 'generate_quizzes_with_gemini.py'))
        spec = importlib.util.spec_from_file_location('generate_quizzes_with_gemini', gemini_path)
        gq_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gq_module)
        generate_quiz = getattr(gq_module, 'generate_quiz')
        recs = generate_quiz(prompt)
        print("\nStudy Recommendations:\n" + str(recs))
    except Exception as e:
        print(f"[Gemini error] {e}")
        recs = None
    # Delete the file after recommendations
    os.remove(wrong_answers_file)
    print(f"[Info] Deleted analysis file: {wrong_answers_file}")
    return recs

# Example usage:
# get_recommendations_from_gemini('Tools/user_analysis/Vince_wrong_20250524_002651_j3zqbwqk.txt')
