
from main import app
from website import auth
import unittest
import requests


class LoginTestCase(unittest.TestCase):
    #Ensure that flask was set up corrently
    def test_response(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Login', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        self.assertIn(b'kidPage', response.data)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(email="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Login', response.data)
    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client()
        tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)


# class KidTestCase(unittest.TestCase):
#     #Ensure that flask was set up corrently
#     URL="http://127.0.0.1:5000/kidPage"
#     def test_1_kid_page(self):
#         r=requests.get(KidTestCase.URL)
#         self.assertEqual(r.status_code,200)
    

if __name__ == '__name__':
    unittest.main()