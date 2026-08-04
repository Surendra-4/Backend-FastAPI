from tests.test_base import client
from app import schemas

def test_create_user():
    response = client.post('/users', json={"email": "saisurendra.patthigulla3@gmail.com", "password": "SURENDRA@453"})
    new_user = schemas.UserResponse(**response.json())
    assert response.json().get("email") == "saisurendra.patthigulla3@gmail.com"
    assert response.status_code == 201