from main import app
from website import auth,db,models
import unittest
import test


class KidPage_Integration_Test_Case(unittest.TestCase):
    admin=test.AdminTestCase()
    login=test.LoginTestCase()
    kid=test.KidTestCase()
    def test_Integration_SignUp_Login(self):
        self.admin.test_Admin_Sign_Up_add_new()
        self.login.test_correct_kidLogin()
        self.admin.test_Admin_User_Managment_Remove() 
    def test_Integration_enterAnimalQuiz_exitQuiz(self):
        self.kid.test_Animal_Category()
        self.kid.test_Finish_Quiz()
    def test_Integration_enterNatureQuiz_exitQuiz(self):
        self.kid.test_Nature_Category()
        self.kid.test_Finish_Quiz()
    def test_Integration_enterMathQuiz_exitQuiz(self):
        self.kid.test_Math_Category()
        self.kid.test_Finish_Quiz()
    def test_Integration_enterHistoryQuiz_exitQuiz(self):
        self.kid.test_History_Category()
        self.kid.test_Finish_Quiz()
    def test_Integration_enterColorQuiz_exitQuiz(self):
        self.kid.test_Color_Category()
        self.kid.test_Finish_Quiz()
    def test_Integration_enterAnimalQuiz_WrongAnswer(self):
        self.kid.test_Animal_Category()
        self.kid.test_Quiz_Answer_Wrong()
    def test_Integration_enterNatureQuiz_WrongAnswer(self):
        self.kid.test_Nature_Category()
        self.kid.test_Quiz_Answer_Wrong()
    def test_Integration_enterMathQuiz_WrongAnswer(self):
        self.kid.test_Math_Category()
        self.kid.test_Quiz_Answer_Wrong()
    def test_Integration_enterHistoryQuiz_WrongAnswer(self):
        self.kid.test_History_Category()
        self.kid.test_Quiz_Answer_Wrong()
    def test_Integration_enterColorQuiz_WrongAnswer(self):
        self.kid.test_Color_Category()
        self.kid.test_Quiz_Answer_Wrong()


class AdminPage_Integration_Test_Case(unittest.TestCase):    
    admin=test.AdminTestCase()
    login=test.LoginTestCase()
    
    def test_Integration_Users_Management(self):
        self.login.test_correct_adminLogin()
        self.admin.test_Admin_User_Managment_response()
    def test_Integration_Content_Management(self):
        self.login.test_correct_adminLogin()
        self.admin.test_Admin_Content_Management_response()
    def test_Integration_Mail_Box(self):
        self.login.test_correct_adminLogin()
        self.admin.test_Admin_MailBox_response()
    def test_Integration_Select_Backgrounds(self):
        self.login.test_correct_adminLogin()
        self.admin.test_Admin_selectBackgrounds_response()
    def test_Integration_AddNewUser_enterUser(self):
        self.login.test_correct_adminLogin()
        self.admin.test_Admin_Sign_Up_add_new()
        self.login.test_correct_kidLogin()
        self.admin.test_Admin_User_Managment_Remove()

# class KidTestCase(unittest.TestCase):
   
    
# class AdminTestCase(unittest.TestCase):
    

# class EditorTestCase(unittest.TestCase):
 

if __name__ == '__name__':
    unittest.main()