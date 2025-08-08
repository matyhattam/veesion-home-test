from unittest.mock import patch
from fastapi import HTTPException

VALID = {
    "uuid": "35df2857-3a48-4985-aed0-e68b5ae4c968",
    "video": "/videos/test_1.avi",
    "timestamp": 1748871320.6882,
    "store": "test-store",
}


def test_alert(client):
    with (
        patch("app.main.fetch_video", return_value=b"bytes"),
        patch("app.main.extract_resolution", return_value="1920x1080"),
    ):
        r = client.post("/alerts", json=VALID)
    assert r.status_code == 200
    assert r.json()["resolution"] == "1920x1080"


def test_validation_422_missing_field(client):
    bad = {k: v for k, v in VALID.items() if k != "store"}
    r = client.post("/alerts", json=bad)
    assert r.status_code == 422


def test_video_server_unreachable_503(client):
    with patch(
        "app.main.fetch_video",
        side_effect=HTTPException(status_code=503, detail="down"),
    ):
        r = client.post("/alerts", json=VALID)
    assert r.status_code == 503


def test_decode_failure_500(client):
    with (
        patch("app.main.fetch_video", return_value=b"whatever"),
        patch(
            "app.main.extract_resolution", side_effect=HTTPException(status_code=500)
        ),
    ):
        r = client.post("/alerts", json=VALID)
    assert r.status_code == 500


def test_duplicate_uid_policy(client):
    with (
        patch("app.main.fetch_video", return_value=b"x"),
        patch("app.main.extract_resolution", return_value="640x480"),
    ):
        r1 = client.post("/alerts", json=VALID)
        r2 = client.post("/alerts", json=VALID)

    assert r2.status_code == 400


def test_unsupported_video_format_400(client):
    invalid_alert = {
        "uuid": "35df2857-3a48-4985-aed0-e68b5ae4c968",
        "video": "/videos/test.txt",
        "timestamp": 1748871320.6882,
        "store": "test-store",
    }

    with patch("app.main.fetch_video", return_value=b"fake_video_data"):
        r = client.post("/alerts", json=invalid_alert)

    assert r.status_code == 422
