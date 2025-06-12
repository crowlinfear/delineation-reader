import csv
import io


def extract_qrs_onsets_from_file(file):
    """
    Takes a file-like object (e.g. from Flask request.files)
    and returns a sorted list of QRS onset times in milliseconds.
    """
    try:
        file.stream.seek(0)
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        reader = csv.reader(stream)
    except Exception as e:
        raise ValueError(f"Failed to process file: {str(e)}")

    qrs_onsets = []
    for row in reader:
        if not row or row[0].strip() != "QRS":
            continue
        try:
            onset = int(row[1])
            qrs_onsets.append(onset)
        except (ValueError, IndexError):
            continue

    qrs_onsets.sort()
    return qrs_onsets
