from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pathlib import Path
from find_similar_items import find_similar_items
from flask import send_from_directory

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "client_dist"

app = Flask(__name__, static_folder=str(FRONTEND_DIST), static_url_path="/")
# allow requests from React
CORS(app)

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


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """Serve the built frontend if it exists."""
    if not FRONTEND_DIST.exists():
        return "Frontend build not found. Run 'npm run build' inside client/.", 404

    requested = FRONTEND_DIST / path
    if path and requested.exists():
        return send_from_directory(str(FRONTEND_DIST), path)

    index_file = FRONTEND_DIST / "index.html"
    if index_file.exists():
        return send_from_directory(str(FRONTEND_DIST), "index.html")

    return "Frontend build missing index.html", 404

if __name__ == "__main__":
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host=host, port=port, debug=debug)