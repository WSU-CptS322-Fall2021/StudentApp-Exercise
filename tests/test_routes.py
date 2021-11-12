"""
This file contains the functional tests for the routes.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import pytest
from app import create_app, db
from app.Model.models import Class, Major, Student
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    db.init_app(flask_app)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

@pytest.fixture
def new_user():
    user = Student(username='sakire', email='sakire@wsu.edu',firstname='Sakire',lastname='Arslan Ay', address='Pullman, WA')
    user.set_password('1234')
    return user

@pytest.fixture
def init_database(request,test_client):
    # Create the database and the database table
    db.create_all()
    # initialize the majors
    if Major.query.count() == 0:
        majors = [{'name':'CptS','department':'School of EECS'},{'name':'SE','department':'Schoolof EECS'},{'name':'EE','department':'School of EECS'},
                  {'name':'ME','department':'Mechanical Engineering'}, {'name':'MATH','department': 'Mathematics'}  ]
        for t in majors:
            db.session.add(Major(name=t['name'],department=t['department']))
        db.session.commit()
    #add a user    
    user1 = Student(username='sakire', email='sakire@wsu.edu',firstname='Sakire',lastname='Arslan Ay', address='Pullman, WA')
    user1.set_password('1234')
    # Insert user data
    db.session.add(user1)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_register_page(request,test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_register(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/register', 
                          data=dict(username='john', email='john@wsu.edu',password="bad-bad-password",password2="bad-bad-password", firstname='John',lastname='Yates', address='Pullman, WA'),
                          follow_redirects = True)
    assert response.status_code == 200

    s = db.session.query(Student).filter(Student.username=='john')
    assert s.first().lastname == 'Yates'
    assert s.count() == 1
    assert b"Please log in to access this page." in response.data
    assert b"Congratulations, you are now a registered user!" in response.data
    assert b"Sign In" in response.data   

def test_invalidlogin(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login', 
                          data=dict(username='sakire', password='12345',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    response = test_client.post('/login', 
                          data=dict(username='sakire', password='1234',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Hi, Sakire Arslan Ay!" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
   

def test_createclass(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing , after user logs in,
    WHEN the '/createclass' page is requested (GET)  AND /createclass' form is submitted (POST)
    THEN check that response is valid and the class is successfully created in the database
    """
    #first login
    response = test_client.post('/login', 
                          data=dict(username='sakire', password='1234',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Hi, Sakire Arslan Ay!" in response.data
    
    #test the "create class" form 
    response = test_client.get('/createclass')
    assert response.status_code == 200
    assert b"Create a new class" in response.data
    
    #test posting a class
    response = test_client.post('/createclass', 
                          data=dict(coursenum = '355', title = 'Programming Languages', major = 'CptS'),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"CptS 355" in response.data
    assert b"Programming Languages" in response.data 
    c = db.session.query(Class).filter(Class.coursenum =='355')
    assert c.first().title == 'Programming Languages'
    assert c.count() == 1

    #finally logout
    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data


def test_enroll(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing , after user logs in, and after a class is created
    WHEN the '/enroll' form is submitted (POST)
    THEN check that response is valid and the currently logged in user (student) is successfully added to roster
    """
    """We will write this test in class."""
    pass

# def test_login(request,test_client,init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/' page is requested (GET)
#     THEN check that the response is valid
#     """
#     response = test_client.post('/login', 
#                           data=dict(username='sakire', password='1234',remember_me=False),
#                           follow_redirects = True)
#     assert response.status_code == 200
#     assert b"Hi, Sakire Arslan Ay!" in response.data
