import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Reads the Gemini API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODELS_URL = 'https://generativelanguage.googleapis.com/v1beta/models'

def list_gemini_models():
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set in environment.")
        return
    params = {'key': GEMINI_API_KEY}
    try:
        response = requests.get(GEMINI_MODELS_URL, params=params, timeout=30)
        response.raise_for_status()
        models = response.json().get('models', [])
        if not models:
            print("No models found or you do not have access to any models.")
            return
        print("Available Gemini models:")
        for model in models:
            print(f"- {model.get('name')} (displayName: {model.get('displayName', 'N/A')})")
    except Exception as e:
        print(f"Error fetching models: {e}")

def main():
    list_gemini_models()

if __name__ == "__main__":
    main()
