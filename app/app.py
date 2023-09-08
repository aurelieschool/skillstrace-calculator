from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
)
from werkzeug.utils import secure_filename
import os
import tempfile
import calc
import pandas as pd
import io
import openpyxl
from openpyxl.styles import NamedStyle

app = Flask(__name__)

file_status = {"ready": False, "data": None}

# TODO: CLEAR CACHES WHEN THE PERSON RELOADS THE PAGE !!!
# TODO: DON'T ENABLE DOWNLOAD BUTTON UNTIL IT'S ACTUALLY READY (NOT JUST FILE STATUS READY)


@app.route("/")
def index():
    return render_template("index.html")


def getScoresSummary(file, assessment_type):
    try:
        file_path = os.path.join(tempfile.gettempdir(), secure_filename(file.filename))
        file.save(file_path)

        file_status["data"] = calc.summaryFromFile(file_path, assessment_type)
        file_status["ready"] = True

        os.remove(file_path)

        return "File succesfully processed"
    except Exception as e:
        return f"Error processing file: {str(e)}"


def get_scores_summary(file, assessment_type):
    try:
        file_path = os.path.join(tempfile.gettempdir(), secure_filename(file.filename))
        file.save(file_path)

        file_status["data"] = calc.report_from_file(file_path, assessment_type)
        file_status["ready"] = True

        os.remove(file_path)

        return "file processed"
    except Exception as e:
        return f"Error processing file: {str(e)}"


@app.route("/processFile", methods=["POST"])
def processFile():
    file = request.files.get("file")
    assessment_type = request.form.get("assessment_type")
    if file and file.filename != "":
        message = get_scores_summary(file, assessment_type)
        if "error" in message:
            return jsonify({"error": message})
        else:
            return jsonify({"message": message})
    else:
        return jsonify({"error": "no file selected or file name empty"})


@app.route("/check_file_status", methods=["GET"])
def check_file_status():
    global file_ready
    if file_status["ready"]:
        return jsonify({"message": "done"})
    else:
        return jsonify({"message": "not done"})


@app.route("/download", methods=["GET"])
def download():
    if file_status["ready"]:
        df = pd.DataFrame(file_status["data"])
        buffer = io.BytesIO()

        percent_style = NamedStyle(name="percent", number_format="0%")

        # Save DataFrame to Excel directly into the buffer
        df.to_excel(buffer, index=True, sheet_name="Sheet1", engine="openpyxl")

        # If you want to apply styles like before, you'll still need to open the workbook with openpyxl
        # and manipulate it, then save it back to the buffer. For simplicity, I've omitted this.

        # back to the start of the buffer
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="results.xlsx",
        )
    else:
        return "No file ready for download"


if __name__ == "__main__":
    app.run(debug=True)
