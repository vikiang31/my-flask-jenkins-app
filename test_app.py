import tempfile
from pathlib import Path

import app as weather_app


def setup_test_db():
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db.close()

    weather_app.DB_PATH = Path(temp_db.name)
    weather_app.init_db()
    weather_app.app.config["TESTING"] = True

    return temp_db.name


def test_home_page():
    db_file = setup_test_db()
    client = weather_app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Weather Tracker App" in response.data


def test_health_endpoint():
    db_file = setup_test_db()
    client = weather_app.app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_get_weather_empty():
    db_file = setup_test_db()
    client = weather_app.app.test_client()

    response = client.get("/weather")

    assert response.status_code == 200
    assert response.get_json() == []


def test_add_weather_record():
    db_file = setup_test_db()
    client = weather_app.app.test_client()

    payload = {
        "city": "Sofia",
        "timestamp": "2026-03-21 18:00",
        "temperature": 16.5,
        "condition": "sunny",
    }

    response = client.post("/weather", json=payload)

    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json["city"] == "Sofia"
    assert response_json["condition"] == "sunny"
    assert response_json["temperature"] == 16.5


def test_get_weather_after_insert():
    db_file = setup_test_db()
    client = weather_app.app.test_client()

    payload = {
        "city": "Sofia",
        "timestamp": "2026-03-21 18:00",
        "temperature": 16.5,
        "condition": "sunny",
    }

    client.post("/weather", json=payload)
    response = client.get("/weather")

    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json) == 1
    assert response_json[0]["city"] == "Sofia"


def test_get_weather_by_city():
    db_file = setup_test_db()
    client = weather_app.app.test_client()

    client.post(
        "/weather",
        json={
            "city": "Sofia",
            "timestamp": "2026-03-21 18:00",
            "temperature": 16.5,
            "condition": "sunny",
        },
    )

    client.post(
        "/weather",
        json={
            "city": "Plovdiv",
            "timestamp": "2026-03-21 19:00",
            "temperature": 18.0,
            "condition": "cloudy",
        },
    )

    response = client.get("/weather/Sofia")

    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json) == 1
    assert response_json[0]["city"] == "Sofia"


def test_add_weather_missing_fields():
    db_file = setup_test_db()
    client = weather_app.app.test_client()

    response = client.post(
        "/weather",
        json={
            "city": "Sofia",
            "temperature": 16.5,
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required fields"}