from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

@pytest.fixture()
def new_user():
    user_data = {"name":"example@gmail.com"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    return new_user

@pytest.mark.parametrize("email", ["rodrigo@gmail.com", "rodrigo@hotmail.com", "rodrigo@msn.com"])
def test_user_valid(email):
    res = client.post("/users/", json = {"name":email})
    assert res.status_code == 201

def test_user_delete_valid(new_user):
    aName = new_user['name']
    res = client.delete("/users/{aName}", json = {"name":aName})
    assert res.status_code == 204