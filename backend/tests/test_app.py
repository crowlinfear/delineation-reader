import io
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_route_valid(client):
    content = "QRS,1000\nQRS,2000\nQRS,3000\n"
    data = {
        "file": (io.BytesIO(content.encode("utf-8")), "test.csv"),
        "start_time": "2025-06-06 00:00:00"
    }
    response = client.post("/delineation", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "mean_hr" in json_data
    assert "min_time" in json_data

def test_route_missing_file(client):
    response = client.post("/delineation", data={}, content_type="multipart/form-data")
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_route_bad_start_time(client):
    content = "QRS,1000\nQRS,2000\nQRS,3000\n"
    data = {
        "file": (io.BytesIO(content.encode("utf-8")), "test.csv"),
        "start_time": "not-a-time"
    }
    response = client.post("/delineation", data=data, content_type="multipart/form-data")
    json_data = response.get_json()
    assert response.status_code == 200
    assert "mean_hr" in json_data
    assert "warning" in json_data

def test_route_valueerror_handler(client):
    # Malformed file that causes UnicodeDecodeError -> ValueError
    bad_bytes = b"\x80\x81\x82"  # invalid UTF-8
    data = {
        "file": (io.BytesIO(bad_bytes), "bad.csv"),
    }

    response = client.post("/delineation", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data
    assert "Failed to process file" in json_data["error"]