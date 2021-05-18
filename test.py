from main import app
from website import auth,db,models
import unittest
from flask import session
from website import db
from website.models import  User, Question, QuestionCategory, MailBox ,Background,Score



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

class KidTestCase(unittest.TestCase):
    def Post_Response_Kid_Page(self):
        tester = app.test_client(self)
        response=tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        return response
    def Post_Response_Quiz_Page(self,category):
        tester = app.test_client(self)
        tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response=tester.post(
            '/kidPage',
            data=dict(cat=category,pick="category"),
            follow_redirects=True
        )
        return response

    def Post_Tester_Quiz_Page(self,category):
        tester = app.test_client(self)
        tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        tester.post(
            '/kidPage',
            data=dict(cat=category,pick="category"),
            follow_redirects=True
        )
        return tester
  
    #Ensure that flask was set up corrently
    def test_Kid_Page_response(self):
        tester = app.test_client(self)
        tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response=tester.get('/kidPage')
        self.assertEqual(response.status_code, 200)
        
    def test_quizzes(self):
        response=self.Post_Response_Kid_Page()
        self.assertIn(b'Animal', response.data)
        self.assertIn(b'Nature', response.data)
        self.assertIn(b'Math', response.data)
        self.assertIn(b'History', response.data)
        self.assertIn(b'Color', response.data)
        
    def test_Animal_Category(self):
        response=self.Post_Response_Quiz_Page("Animal")
        self.assertIn(b'Animal Questions', response.data)
       
    def test_Nature_Category(self):
        response=self.Post_Response_Quiz_Page("Nature")
        self.assertIn(b'Nature Questions', response.data)
    
    def test_Math_Category(self):
        response=self.Post_Response_Quiz_Page("Math")
        self.assertIn(b'Math Questions', response.data)
    
    def test_History_Category(self):
        response=self.Post_Response_Quiz_Page("History")
        self.assertIn(b'History Questions', response.data) 

    def test_Color_Category(self):
        response=self.Post_Response_Quiz_Page("Color")
        self.assertIn(b'Color Questions', response.data) 
    def test_Finish_Quiz(self):
        tester=self.Post_Tester_Quiz_Page("Animal")
        response=tester.post(
            '/question',
            data=dict(finish1="1"),
            follow_redirects=True
        )
        self.assertIn(b'kidPage', response.data) 

    def test_Quiz_Answer_Wrong(self):
        tester=self.Post_Tester_Quiz_Page("Animal")
        response=tester.post(
            '/question',
            data=dict(q_answer=""),
            follow_redirects=True
        )
        self.assertIn(b'info', response.data)
    def test_InfoPage_BackToKidPage(self):
        tester=self.Post_Tester_Quiz_Page("Animal")
        tester.post(
            '/question',
            data=dict(q_answer=""),
            follow_redirects=True
        )
        response=tester.post(
            '/info',
            data=dict(kidPage=""),
            follow_redirects=True
        )
        self.assertIn(b'kidPage', response.data)
            
    def test_kid_logout(self):
        tester = app.test_client()
        tester.post(
            '/',
            data=dict(email="kid@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)
    
    
class AdminTestCase(unittest.TestCase):
    def Post_Response_Admin_Page(self):
        tester = app.test_client(self)
        response=tester.post(
            '/',
            data=dict(email="admin@gmail.com", password="1234567"),
            follow_redirects=True
        )
        return response
    def Post_tester_Admin_Page(self):
        tester = app.test_client(self)
        tester.post(
            '/',
            data=dict(email="admin@gmail.com", password="1234567"),
            follow_redirects=True
        )
        return tester

    def test_Admin_Page_response(self):
        response=self.Post_Response_Admin_Page()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'adminPage', response.data)


    def test_Admin_User_Managment_response(self):
        tester=self.Post_tester_Admin_Page()
        response=tester.get('/userManagment', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'userManagment', response.data)

    def test_Admin_User_Managment_Edit(self):
        tester=self.Post_tester_Admin_Page()
        tester.get('/userManagment', follow_redirects=True)
        response=tester.post(
            '/userManagment',
            data=dict(editphide="1",editId="3",first_name="kid",email="kid@gmail.com",password="1234567",auth="kid"),
            follow_redirects=True
        )
        self.assertIn(b'userManagment', response.data) 
    
    def test_Admin_User_Managment_Remove(self):
        tester=self.Post_tester_Admin_Page()
        tester.get('/userManagment', follow_redirects=True)
        response=tester.post(
            '/userManagment',
            data=dict(deletephide="1",deleteId="8"),
            follow_redirects=True
        )
        self.assertIn(b'userManagment', response.data) 

    def test_Admin_Sign_Up_add_new(self):
        tester=self.Post_tester_Admin_Page()
        tester.get('/userManagment', follow_redirects=True)
        response=tester.post(
            '/userManagment',
            data=dict(addphide="1",add_email="kid4@gmail.com",add_firstname="kid4",
            add_password1="1234567",add_password2="1234567",add_auth="kid"),
            follow_redirects=True
        )
        self.assertIn(b'userManagment', response.data)

    def test_Admin_Sign_Up_add_existing_user(self):
        tester=self.Post_tester_Admin_Page()
        tester.get('/userManagment', follow_redirects=True)
        response=tester.post(
            '/userManagment',
            data=dict(addphide="1",add_email="kid@gmail.com",add_firstname="kid",
            add_password1="1234567",add_password2="1234567",add_auth="kid"),
            follow_redirects=True
        )
        self.assertIn(b'userManagment', response.data)

    def test_Admin_Content_Management_response(self):
        tester=self.Post_tester_Admin_Page()
        response=tester.get('/contentManagement', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'contentManagement', response.data)
    
    def test_Admin_MailBox_response(self):
        tester=self.Post_tester_Admin_Page()
        response=tester.get('/mailBox', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'mailBox', response.data)

    def test_Admin_selectBackgrounds_response(self):
        tester=self.Post_tester_Admin_Page()
        response=tester.get('/selectBackgrounds', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'selectBackgrounds', response.data)

    def test_Admin_Add_User_response(self):
        tester=self.Post_tester_Admin_Page()
        response=tester.get('/userManagment', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'userManagment', response.data)

    def test_Admin_logout(self):
        tester=self.Post_tester_Admin_Page()
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)


class EditorTestCase(unittest.TestCase):
    #Ensure that flask was set up corrently
    def test_Editor_Page_response(self):
        tester = app.test_client(self)
        tester.post(
            '/',
            data=dict(email="editor@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response=tester.get('/editorPage')
        self.assertEqual(response.status_code, 200)

    def test_editor_logout(self):
        tester = app.test_client()
        tester.post(
            '/',
            data=dict(email="editor@gmail.com", password="1234567"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)
    

if __name__ == '__name__':
    unittest.main()