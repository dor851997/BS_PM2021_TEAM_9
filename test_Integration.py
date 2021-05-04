from main import app
from website import auth,db,models
import unittest
import test


class Login_Integration_Test_Case(unittest.TestCase):
    admin=test.AdminTestCase()
    login=test.LoginTestCase()
    def test_Integration_SignUp_Login_Remove(self):
        self.admin.test_Admin_Sign_Up_add_new()
        self.login.test_correct_kidLogin()
        self.admin.test_Admin_User_Managment_Remove()




# class KidTestCase(unittest.TestCase):
   
    
# class AdminTestCase(unittest.TestCase):
    

# class EditorTestCase(unittest.TestCase):
 

if __name__ == '__name__':
    unittest.main()