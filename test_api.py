import requests

# Base URL for API
BASE_URL = "http://127.0.0.1:8000"


def test_get_weather_success():
    # Test for success request
    city = "Moscow"
    response = requests.get(f"{BASE_URL}/weather/{city}")

    assert response.status_code == 200

    data = response.json()
    assert "city" in data
    assert "country" in data
    assert "temperature" in data
    assert "weather_description" in data
    assert "icon" in data


def test_get_weather_city_not_found():
    # Test for case city not found
    city = "NonexistentCity"
    response = requests.get(f"{BASE_URL}/weather/{city}")

    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "City not found"
