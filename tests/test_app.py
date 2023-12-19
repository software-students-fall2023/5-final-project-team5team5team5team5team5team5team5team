# pylint: disable=redefined-outer-name
import pytest
from web_app.app import app, users
from flask import session
from werkzeug.security import check_password_hash


@pytest.fixture
def test_client():
    # Directly use the app instance since there's no factory function
    app.config["TESTING"] = True  # Enable testing mode
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


def test_signup_route_get(test_client):
    response = test_client.get("/signup")
    assert response.status_code == 200
    # Update assertion to check for content within the returned HTML
    assert b"<title>Signup</title>" in response.data


def test_signup_route_post_existing_user(test_client, mocker):
    mocker.patch("web_app.app.users.find_one", return_value={"username": "testuser"})
    response = test_client.post(
        "/signup",
        data={"username": "testuser", "password": "testpass"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with test_client.session_transaction() as sess:
        assert "Username already exists." in sess["_flashes"][0][1]


def test_signup_route_post_new_user(test_client, mocker):
    mocker.patch("web_app.app.users.find_one", return_value=None)
    mocker.patch("web_app.app.users.insert_one", return_value=None)
    response = test_client.post(
        "/signup",
        data={"username": "newuser", "password": "newpass"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert (
        b"Registration successful." in response.data
    )  # Assuming the flash message is rendered in the HTML


def test_login_route_get(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"<title>Login</title>" in response.data


def test_login_route_post_invalid_credentials(test_client, mocker):
    mocker.patch("web_app.app.users.find_one", return_value=None)
    response = test_client.post(
        "/login", data={"username": "wronguser", "password": "wrongpass"}
    )
    assert response.status_code == 200
    assert b"Invalid credentials." in response.data


def test_login_route_post_valid_credentials(test_client, mocker):
    mocker.patch(
        "web_app.app.users.find_one",
        return_value={"username": "testuser", "password": "hashedpass"},
    )
    mocker.patch("web_app.app.check_password_hash", return_value=True)
    response = test_client.post(
        "/login", data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 302
    assert "/main" in response.headers["Location"]


def test_logout_route(test_client):
    # Simulate login if necessary
    with test_client.session_transaction() as sess:
        sess["_user_id"] = "some_user_id"
        sess[
            "_fresh"
        ] = True  # Flask-Login checks for '_fresh' in session during logout
    response = test_client.get("/logout")
    assert response.status_code == 302
    # Check the session after the logout request
    with test_client.session_transaction() as sess:
        assert "user_id" not in sess
