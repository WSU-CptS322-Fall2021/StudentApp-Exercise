import warnings
warnings.filterwarnings("ignore")

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import Student, Class, Major
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    
class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Student(username='john', firstname='John', lastname='Yates')
        u.set_password('covid')
        self.assertFalse(u.check_password('flu'))
        self.assertTrue(u.check_password('covid'))

    def test_enroll(self):
        m1 = Major(name='CptS', department='EECS')
        db.session.add(m1)
        db.session.commit()
        u1 = Student(username='john', email='john.yates@wsu.com')
        c1 = Class(major='CptS', coursenum='355')
        db.session.add(u1)
        db.session.add(c1)
        db.session.commit()
        self.assertEqual(u1.classes, [])
        self.assertEqual(c1.roster, [])

        u1.enroll(c1)
        db.session.commit()
        self.assertTrue(u1.is_enrolled(c1))
        self.assertEqual(len(u1.classes), 1)
        self.assertEqual(u1.classes[0].classenrolled.coursenum, '355')
        self.assertEqual(u1.classes[0].classenrolled.major, 'CptS')
        self.assertEqual(len(c1.roster), 1)
        self.assertEqual(c1.roster[0].studentenrolled.username, 'john')

        u1.unenroll(c1)
        db.session.commit()
        self.assertFalse(u1.is_enrolled(c1))
        self.assertEqual(len(u1.classes), 0)
        self.assertEqual(len(c1.roster), 0)

    

if __name__ == '__main__':
    unittest.main(verbosity=2)