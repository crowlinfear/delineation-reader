from utils.time_utils import get_offset_time_str

def test_valid_offset_time():
    result = get_offset_time_str("2025-06-06 00:00:00", 2000)
    assert result == "2025-06-06 00:00:02 UTC"

def test_invalid_time_string():
    result = get_offset_time_str("not-a-time", 1000)
    assert result is None
