from datetime import datetime, timedelta, timezone


def parse_start_time_utc(start_time_str):
    """Parses a timestamp string into a UTC datetime object.

    Returns None if the format is invalid.
    """
    try:
        base_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        return base_time.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def get_offset_time_str(start_time_str, offset_ms):
    """
    Returns a UTC-formatted string for a timestamp offset from a start time.
    """
    base = parse_start_time_utc(start_time_str)
    if base is None:
        return None
    return (base + timedelta(milliseconds=offset_ms)).strftime("%Y-%m-%d %H:%M:%S UTC")
