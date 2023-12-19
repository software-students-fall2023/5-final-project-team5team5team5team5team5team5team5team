import unittest
from flask import Flask
from web_app.app import app, users, User, generate_password_hash

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        # set up a test client and db
        self.app = app.test_client()
        self.db = app.config['DATABASE']

    def tearDown(self):
        #reset
        self.db.users.drop()

    def test_signup(self):
        # test user registration

        # make a POST request to the signup route with test data
        response = self.app.post('/signup', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)

        # check if registration was successful
        self.assertIn(b'Registration successful.', response.data)

        # check if the user is now in the db
        user_in_db = self.db.users.find_one({"username": "testuser"})
        self.assertIsNotNone(user_in_db)

    def test_login(self):
        # test user login

        # create a test user in the db
        hashed_password = generate_password_hash('testpassword')
        self.db.users.insert_one({"username": "testuser", "password": hashed_password})

        # make a POST request to the login route with test data
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)

        # check if login was successful
        self.assertIn(b'Welcome, testuser!', response.data)

        # check if the current user is logged in
        with self.app as c:
            with c.session_transaction() as sess:
                sess['_user_id'] = 'testuser'
            response = self.app.get('/main', follow_redirects=True)
            self.assertIn(b'Welcome, testuser!', response.data)

    def test_invalid_login(self):
        # test invalid user login

        # make a POST request to the login route with incorrect credentials
        response = self.app.post('/login', data=dict(
            username='nonexistentuser',
            password='incorrectpassword'
        ), follow_redirects=True)

        # check if error message is displayed
        self.assertIn(b'Invalid credentials.', response.data)

if __name__ == '__main__':
    unittest.main()
