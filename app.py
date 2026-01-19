import os
import logging
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from analyzer.log_analyzer import ServerLogAnalyzer


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_FOLDER, "debug.log")

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("log-analyzer-app")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "replace-with-secure-key"


@app.route("/", methods=["GET"])
def index():
    """Upload page."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Handle upload and trigger analysis."""
    upload = request.files.get("logfile")
    if upload is None or upload.filename.strip() == "":
        logger.warning("No file provided in upload request")
        return redirect(url_for("index"))

    filename = secure_filename(upload.filename)
    saved_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Save uploaded file safely
    upload.save(saved_path)
    logger.info("Saved upload to %s", saved_path)

    analyzer = ServerLogAnalyzer(saved_path)
    results = analyzer.analyze()

    return render_template(
        "dashboard.html",
        total_requests=results["total_requests"],
        status_counts=results["status_counts"],
        malformed_lines=results["malformed_lines"],
        filename=filename,
    )


if __name__ == "__main__":
    app.run(debug=True)
