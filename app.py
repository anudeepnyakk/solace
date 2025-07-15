from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")

print(f"API Key: {OPENROUTER_API_KEY}")  # Debug print

@app.route('/improve', methods=['POST'])
def improve_text():
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' in request body"}), 400

        text = data.get('text', '')
        action = data.get('action', 'rewrite')
        prompt = f"{action}: {text}"

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek/deepseek-r1:free",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=10
        )
        response.raise_for_status()
        return jsonify({"improvedText": response.json()["choices"][0]["message"]["content"]})

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": "API request failed", "details": response.json() if response.content else {"message": str(http_err)}}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)