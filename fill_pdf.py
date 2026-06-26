import os
import io
import re
from flask import Flask, request, send_file, jsonify, send_from_directory
from fill_pdf import fill_invoice_pdf

app = Flask(__name__, static_folder="static")


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


@app.route("/api/generate-invoice", methods=["POST", "OPTIONS"])
def generate_invoice():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(force=True, silent=True) or {}

    required = ["invoice_no", "date"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        pdf_bytes = fill_invoice_pdf(data)
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {e}"}), 500

    safe_invoice_no = re.sub(r"[^A-Za-z0-9_-]+", "_", data.get("invoice_no", "output"))
    filename = f"Invoice_{safe_invoice_no}.pdf"
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
