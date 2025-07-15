import os
import requests
import time

def get_gemini_response(input_text, pdf_text, prompt, max_retries=3, retry_delay=2):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "API key is missing. Make sure it's set in the .env file."}
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {"parts": [
                {"text": input_text},
                {"text": pdf_text},
                {"text": prompt}
            ]}
        ]
    }
    for attempt in range(max_retries):
        response = requests.post(f"{url}?key={api_key}", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return {"error": "The model is overloaded. Please try again later. (503)"}
        else:
            return {"error": response.text}
    return {"error": "Failed to get a response from the Gemini API after several attempts."} 