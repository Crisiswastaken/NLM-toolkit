import os
import subprocess
from config import RECOMMEND_PROMPT, RECOMMENDATION_MODEL  # Use the same model as summarization, or set a new one if needed

def get_recommendations_from_llm(wrong_answers_file):
    with open(wrong_answers_file, 'r', encoding='utf-8') as f:
        wrong_answers = f.read()
    prompt = f"""{RECOMMEND_PROMPT}\n---\n{wrong_answers}\n\n### Recommendations:\n"""
    try:
        result = subprocess.run(
            ["ollama", "run", RECOMMENDATION_MODEL],
            input=prompt.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120
        )
        if result.returncode != 0:
            print(f"[Ollama error] {result.stderr.decode('utf-8')}")
            return None
        recs = result.stdout.decode('utf-8').strip()
        print("\nStudy Recommendations:\n" + recs)
    except Exception as e:
        print(f"[Ollama subprocess error] {e}")
        recs = None
    # Delete the file after recommendations
    os.remove(wrong_answers_file)
    print(f"[Info] Deleted analysis file: {wrong_answers_file}")
    return recs

# Example usage:
# get_recommendations_from_llm('Tools/user_analysis/Vince_wrong_20250524_002651_j3zqbwqk.txt')
