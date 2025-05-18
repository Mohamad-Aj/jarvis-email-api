from flask import Flask, request, jsonify
from email_writer import generate_email
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/generate_email", methods=["POST"])
def handle_request():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        result = generate_email(prompt)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/health")
def health():
    return "ok", 200


if __name__ == "__main__":
    app.run()
