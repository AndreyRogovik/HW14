from unittest.mock import MagicMock, patch

import pytest

from src.database.models import User
from src.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


# def test_create_contact(client, token):
#     with patch.object(auth_service, 'r') as r_mock:
#         r_mock.get.return_value = None
#         response = client.post(
#             "/api/contacts",
#             json={
#                 "first_name": "Rokky",
#                 "last_name": "Balboa",
#                 "email": "Roky@Balboa.com",
#                 "phone": "+14155552671",
#                 "birthday": "1950-01-01",
#                 "addtitional_data": "Boxer"
#             },
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         assert response.status_code == 201, response.text
#         data = response.json()
#         assert data["first_name"] == "Rokky"
#         assert "id" in data


def test_get_contacts(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert len(data) == 1
        assert "id" in data[0]
    #
#
# def test_get_contact(client, contact):
#     response = client.get("/api/contacts/1")
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["first_name"] == contact.get("first_name")
#     assert "id" in data
#
#
# def test_get_contact_not_found(client):
#     response = client.get("/api/contacts/2")
#     assert response.status_code == 404, response.text
#     data = response.json()
#     assert data["detail"] == "Not found"
#
#
# def test_update_contact_found(client, updated_contact):
#     response = client.put("/api/contacts/1", json=updated_contact)
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["first_name"] == updated_contact.get("first_name")
#     assert data["last_name"] == updated_contact.get("last_name")
#     assert data["additional_data"] == updated_contact.get("additional_data")
#     assert "id" in data
#
#
# def test_update_contact_not_found(client, updated_contact):
#     response = client.put("/api/contacts/2", json=updated_contact)
#     assert response.status_code == 404, response.text
#     data = response.json()
#     assert data["detail"] == "Not found"
#
#
# def test_remove_contact(client, updated_contact):
#     response = client.delete("/api/contacts/1")
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["first_name"] == updated_contact.get("first_name")
#     assert "id" in data
#
#
# def test_delete_contact_not_found(client):
#     response = client.delete("/api/contacts/1")
#     assert response.status_code == 404, response.text
#     data = response.json()
#     assert data["detail"] == "Not found"