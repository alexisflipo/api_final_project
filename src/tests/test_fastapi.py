from src.app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_index_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_predict_route():
    test = "test"
    response = client.get(f"/predict?q={test}")
    assert response.status_code == 200
    assert response.json() == {"hello": test}


def test_failure_predict():
    response = response = client.get("/predict")
    print(response)
    assert response.status_code == 400
    assert response.json() == {"detail": "Bad request, the query is missing or invalid"}
