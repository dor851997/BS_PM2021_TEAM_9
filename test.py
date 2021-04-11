from main import app
from website import auth,db,models
import unittest



class LoginTestCase(unittest.TestCase):
    
    #Ensure that flask was set up corrently
    def test_Login_response(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Login', response.data)

    #Ensure login behaves correctly with correct credentials
    def test_correct_kidLogin(self):
        tester = app.test_client()
        response =tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        self.assertIn(b'kidPage', response.data)

    def test_correct_adminLogin(self):
        tester = app.test_client()
        response =tester.post(
            '/',
            data=dict(email="admin@gmail.com", password="1234567"),
            follow_redirects=True
        )
        self.assertIn(b'adminPage', response.data)

    def test_correct_editorLogin(self):
        tester = app.test_client()
        response =tester.post(
            '/',
            data=dict(email="editor@gmail.com", password="1234567"),
            follow_redirects=True
        )
        self.assertIn(b'editorPage', response.data)   

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(email="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Login', response.data)
    #Ensure logout behaves correctly
    def test_quizzes(self):
        tester = app.test_client()
        response=tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        self.assertIn(b'Animal', response.data)
        self.assertIn(b'Nature', response.data)
        self.assertIn(b'Math', response.data)
        self.assertIn(b'History', response.data)
        self.assertIn(b'Color', response.data)
        
    def test_Animal_Category(self):
        tester = app.test_client()
        response=tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response=tester.post(
            '/kidPage',
            data=dict(cat="Animal"),
            follow_redirects=True
        )
        self.assertIn(b'Animal Questions', response.data)
       
    def test_Nature_Category(self):
        tester = app.test_client()
        response=tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response=tester.post(
            '/kidPage',
            data=dict(cat="Nature"),
            follow_redirects=True
        )
        self.assertIn(b'Nature Questions', response.data)
    
    def test_Math_Category(self):
        tester = app.test_client()
        response=tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response=tester.post(
            '/kidPage',
            data=dict(cat="Math"),
            follow_redirects=True
        )
        self.assertIn(b'Math Questions', response.data)
    
    def test_History_Category(self):
        tester = app.test_client()
        response=tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response=tester.post(
            '/kidPage',
            data=dict(cat="History"),
            follow_redirects=True
        )
        self.assertIn(b'History Questions', response.data) 

    def test_Color_Category(self):
        tester = app.test_client()
        response=tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response=tester.post(
            '/kidPage',
            data=dict(cat="Color"),
            follow_redirects=True
        )
        self.assertIn(b'Color Questions', response.data) 


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