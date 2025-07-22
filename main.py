import os
from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder='Static New')
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/grade", methods=["POST"])
def grade():
    data = request.get_json()
    if not data or not all(k in data for k in ('subject','task','student_text')):
        return jsonify({"error": "Missing fields"}), 400

    prompt = (
      f"You are an expert {data['subject']} teacher.\n"
      f"Task: {data['task']}\n"
      f"Student text: {data['student_text']}\n"
      "Give a mark (0‑8) and short feedback."
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return jsonify({"result": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return send_from_directory('Static New', 'Index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
