from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from find_similar_items import find_similar_items
from flask import send_from_directory

app = Flask(__name__)
CORS(app)  # allow requests from React

@app.route("/api/search", methods=["POST"])
def search():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file:
        filepath = os.path.join("query.jpg")
        uploaded_file.save(filepath)

        results = find_similar_items("query.jpg", return_results=True)
        return jsonify(results)

    return jsonify({"error": "Upload failed"}), 400

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(debug=True)
