"""test_app"""
# pylint: disable=redefined-outer-name
import pytest
from web_app.app import app

# from flask import session
# from werkzeug.security import check_password_hash


@pytest.fixture
def test_client():
    """
    The function `test_client()` sets up a testing client for a Flask application.
    """
    # Directly use the app instance since there's no factory function
    app.config["TESTING"] = True  # Enable testing mode
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


def test_signup_route_get(test_client):
    """
    The function tests the GET request to the "/signup" route and checks
    if the response status code is 200 and if the returned HTML contains
    the title "Signup".

    :param test_client: The `test_client` parameter is an instance of the Flask
    test client. It allows you to simulate requests to your Flask application
    during testing. You can use it to send HTTP
    requests and receive responses, just like you would with a regular client
    """
    response = test_client.get("/signup")
    assert response.status_code == 200
    # Update assertion to check for content within the returned HTML
    assert b"<title>Signup</title>" in response.data


def test_signup_route_post_existing_user(test_client, mocker):
    """
    The function tests the behavior of the signup route when a user tries to sign up
    with an existing
    username.

    :param test_client: The `test_client` parameter is an instance of the Flask test
    client. It allows you to make HTTP requests to your Flask application in a
    testing environment

    :param mocker: The `mocker` parameter is a fixture provided by the `pytest-mock`
    library. It allows
    you to mock or patch objects and functions during testing. In this case, it is
    used to mock the
    `find_one` function from the `users` module
    """
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
    """
    The function tests the POST request to the "/signup" route for creating
    a new user and checks if the
    registration was successful.

    :param test_client: The `test_client` parameter is a test client object
    that allows you to make requests to your Flask application in a testing
    environment.

    :param mocker: The `mocker` parameter is a pytest fixture that allows
    you to mock objects and
    functions for testing purposes. In this case, it is used to mock the
    `find_one` and `insert_one` functions from the `users` collection in the database
    """
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
    """
    The function tests the GET request to the "/login" route and checks
    if the response status code is
    200 and if the response data contains the title "Login".

    :param test_client: The `test_client` parameter is an instance of the Flask
    test client. It allows
    you to simulate requests to your Flask application during testing. You can
    use it to send HTTP
    requests and receive responses, just like you would with a regular client
    """
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"<title>Login</title>" in response.data


def test_login_route_post_invalid_credentials(test_client, mocker):
    """
    The function tests the login route by sending a POST request with invalid
    credentials and asserts
    that the response status code is 200 and the response data contains the message
    "Invalid credentials.".

    :param test_client: The `test_client` parameter is an instance of the Flask
    test client. It allows
    you to simulate HTTP requests to your Flask application during testing

    :param mocker: The `mocker` parameter is a pytest fixture that allows you to
    mock objects and
    functions for testing purposes. In this case, it is used to mock the
    `find_one` function from the
    `users` module
    """
    mocker.patch("web_app.app.users.find_one", return_value=None)
    response = test_client.post(
        "/login", data={"username": "wronguser", "password": "wrongpass"}
    )
    assert response.status_code == 200
    assert b"Invalid credentials." in response.data


def test_login_route_post_valid_credentials(test_client, mocker):
    """
    The function tests the login route by mocking the find_one and
    check_password_hash functions, and
    then sending a POST request with valid credentials.

    :param test_client: The `test_client` parameter is an instance of the
    Flask test client. It allows
    you to send HTTP requests to your Flask application and receive the
    responses for testing purposes

    :param mocker: The `mocker` parameter is a pytest fixture that provides
    a way to mock objects and
    functions during testing. It allows you to replace the implementation
    of a function or object with a
    mock version, which can be useful for isolating specific parts of your
    code during testing
    """
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
    """
    The function tests the logout route by simulating a login, making
    a GET request to the logout route,
    and then checking the session to ensure that the user ID is no
    longer present.

    :param test_client: The `test_client` parameter is an instance of
    Flask's `TestClient` class. It is
    used to simulate requests to your Flask application during testing.
    You can use it to send HTTP
    requests and receive responses, just like you would with a regular client
    """
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


def test_saved_recipes(test_client):
    """
    The function tests the saved recipes route by simulating a login, making
    a GET request to the saved recipes route,
    and then checking the session to ensure that the user ID is present.

    :param test_client: The `test_client` parameter is an instance of
    Flask's `TestClient` class. It is
    used to simulate requests to your Flask application during testing.
    You can use it to send HTTP
    requests and receive responses, just like you would with a regular client
    """
    # Simulate login if necessary
    with test_client.session_transaction() as sess:
        sess["_user_id"] = "some_user_id"
        sess["_fresh"] = True  # Flask-Login checks for '_fresh' in session during logout
    
    # Make a GET request to the saved recipes route
    response = test_client.get("/show_saved_recipes")

    # Check if the response is a redirection (status code 302)
    assert response.status_code == 302
    
    # Check if the redirection is to the login page
    assert "/login" in response.headers["Location"]
    
    # Check if the intended destination is "/show_saved_recipes"
    assert "next=%2Fshow_saved_recipes" in response.headers["Location"]
