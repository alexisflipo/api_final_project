from src.app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_index_route():
    response = client.get("/")
    print(response)
    assert response.status_code == 200


def test_not_valid_value():
    response = client.get(
        "/predict?country=europe&remote_ratio=&xp_encoded=2&company_size=2"
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "remote_ratio"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_missing_value():
    reponse = client.get("predict?remote_ratio=100&xp_encoded=2&company_size=2")
    assert reponse.json() == {
        "detail": [
            {
                "loc": ["query", "country"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_predict_route():
    response = client.get(
        f"/predict?country=europe&remote_ratio=100&xp_encoded=2&company_size=2"
    )
    assert response.status_code == 200


def test_failure_predict():
    response = response = client.get("/predict")
    assert response.status_code == 422
