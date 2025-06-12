from flask import Flask, request, jsonify, send_from_directory
from utils.heart_rate import compute_heart_rate_stats
from utils.file_utils import extract_qrs_onsets_from_file

app = Flask(__name__, static_folder="static", static_url_path="")



@app.errorhandler(ValueError)
def handle_error(error):
    return jsonify({"error": str(error)}), 400


@app.route('/')
@app.route('/<path:path>')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')



@app.route('/delineation', methods=['POST'])
def upload_file():
    # getting data from user
    input_file = request.files.get('file')
    start_time = request.form.get('start_time')

    if not input_file:
        return jsonify({"error": "No file uploaded"}), 400


    qrs_onsets = extract_qrs_onsets_from_file(input_file)

    stats = compute_heart_rate_stats(qrs_onsets, start_time=start_time)

    return jsonify(stats), 200

if __name__ == '__main__':
    app.run(debug=True)
