from utils.time_utils import get_offset_time_str


def compute_heart_rate_stats(qrs_onsets, start_time=None):
    """Computes mean, minimum, and maximum heart rate from QRS onset times.

    Optionally returns corresponding timestamps if a start time is provided.
    """
    if len(qrs_onsets) < 2:
        return {"error": "Not enough QRS data to compute heart rate."}

    rr_intervals = [
        qrs_onsets[i] - qrs_onsets[i - 1] for i in range(1, len(qrs_onsets))
    ]
    heart_rates = [60000 / rr for rr in rr_intervals if rr > 0]

    mean_hr = sum(heart_rates) / len(heart_rates)
    min_hr = min(heart_rates)
    max_hr = max(heart_rates)

    min_index = heart_rates.index(min_hr)
    max_index = heart_rates.index(max_hr)

    min_time = qrs_onsets[min_index + 1]
    max_time = qrs_onsets[max_index + 1]

    result = {
        "mean_hr": round(mean_hr, 2),
        "min_hr": round(min_hr, 2),
        "min_time_ms": min_time,
        "max_hr": round(max_hr, 2),
        "max_time_ms": max_time,
    }

    if start_time:
        result["min_time"] = get_offset_time_str(start_time, min_time)
        result["max_time"] = get_offset_time_str(start_time, max_time)

        if result["min_time"] is None or result["max_time"] is None:
            result["warning"] = "Invalid start time format"

    return result
