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

        # Create a buffer to store the Excel file in memory
        buffer = io.BytesIO()

        # Define a percentage style
        percent_style = NamedStyle(name="percent", number_format="0%")

        # Write the dataframe to Excel
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=True, sheet_name="Sheet1")
            worksheet = writer.sheets["Sheet1"]

            # Apply the percentage style to 'Value' column
            for row in worksheet.iter_rows(
                min_row=2, min_col=2, max_col=2, max_row=worksheet.max_row
            ):  # assuming Value is the second column and you have a header row
                for cell in row:
                    if isinstance(
                        cell.value, float
                    ):  # assuming your percentages are floats like 0.75 for 75%
                        # cell.value *= 100  # convert to percentage
                        cell.style = percent_style

            # Auto-size columns
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = max_length + 2
                worksheet.column_dimensions[
                    column[0].column_letter
                ].width = adjusted_width

        # Go back to the start of the buffer
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
