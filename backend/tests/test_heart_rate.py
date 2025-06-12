from utils.heart_rate import compute_heart_rate_stats

def test__qrs_onsets():
    qrs = [1000, 2000, 3000]
    result = compute_heart_rate_stats(qrs)
    assert "mean_hr" in result
    assert "min_time_ms" in result
    assert "min_time" not in result
    assert result["mean_hr"] == 60.0

    # test with start_time arg not None
    result = compute_heart_rate_stats(qrs, start_time="2025-06-06 00:00:00")
    assert "mean_hr" in result
    assert "min_time_ms" in result
    assert "min_time" in result
    assert result["min_time"] is not None
    assert result["mean_hr"] == 60.0

    # test with invalid start_time
    result = compute_heart_rate_stats(qrs, start_time="not-a-time")
    
    assert "mean_hr" in result
    assert result["min_time"] is None
    assert "warning" in result
    assert result["warning"] == "Invalid start time format"

def test_not_enough_data():
    qrs = [1000]
    result = compute_heart_rate_stats(qrs)
    assert "error" in result
    assert result["error"] == "Not enough QRS data to compute heart rate."