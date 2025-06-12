from utils.file_utils import extract_qrs_onsets_from_file
from werkzeug.datastructures import FileStorage
import io
import pytest

def test_extract_qrs_onsets():
    content = "QRS,1000\nP,1500\nQRS,2000\nQRS,3000\n"
    file = FileStorage(stream=io.BytesIO(content.encode("utf-8")))
    result = extract_qrs_onsets_from_file(file)
    assert result == [1000, 2000, 3000]


def test_bad_input_file():
    bad_bytes = b'\x80\x81\x82'  # Invalid UTF-8
    file = FileStorage(stream=io.BytesIO(bad_bytes))

    with pytest.raises(ValueError) as exc_info:
        extract_qrs_onsets_from_file(file)

    assert "Failed to process file" in str(exc_info.value)


def test_sbad_rows():
    content = (
        "QRS,1000\n"          # valid
        "QRS,\n"              # IndexError (missing onset)
        "QRS,notanumber\n"    # ValueError (non-int)
        "P,2000\n"            # ignored (not QRS)
        "QRS,3000\n"          # valid
    )

    file = FileStorage(stream=io.BytesIO(content.encode("utf-8")))
    result = extract_qrs_onsets_from_file(file)

    # Only the two valid QRS onsets should be included
    assert result == [1000, 3000]