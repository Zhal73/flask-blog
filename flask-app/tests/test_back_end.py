import unittest

from flask import url_for
from flask_testing import TestCase

from application import app, db, bcrypt
from application.models import Users, Posts

from os import getenv

# the TestBase class contains all the necassary
# setup configuration so that the tests can be run
# and the test that will be performed
class TestBase(TestCase):
    pass
    def create_app(self):
        # pass in configurations for test database
        # this allows the test suite to connect to the database
        # using the environment variable we set when we activate the venmv
        # inside the VM
        config_name = 'testing'
        app.config.update(SQLALCHEMY_DATABASE_URI=getenv('TEST_DB_URI'),
                SECRET_KEY=getenv('TEST_SECRET_KEY'),
                WTF_CSRF_ENABLED=False,
                DEBUG=True
                )
        return app

    def setUp(self):
        # this will be called every time we run a test
        # ensure there is no data in the test database when the test starts
        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        hashed_pw = bcrypt.generate_password_hash('admin2016')
        admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password=hashed_pw)

        # create test non-admin user
        hashed_pw_2 = bcrypt.generate_password_hash('test2016')
        employee = Users(first_name="test", last_name="user", email="test@user.com", password=hashed_pw_2)  

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        # this will be called AFTER every test
        # this to make sure that every time we run a test
        # the database is empty and there are no duplicate
        # posts that can cause proble to the test performed.
        db.session.remove()
        db.drop_all()
##### ACTUAL TESTS ########
class TestViews(TestBase):
    pass
    def test_homepage_view(self):
        # this tests if the homepage is accessible
        # by anyone, without the needs for a
        # user to be logged in
        # tests line 10,13 and 14 of routes.py
        response = self.client.get(url_for('home')) #call the home page
        self.assertEqual(response.status_code, 200) #checks if it is accessible. code : 200
    
    def test_add_new_post(self):
        # this tests that once a user posts a new post,
        # the user is then redirected to the home page
        # and the new post is visible
        # test line 11-12,23-36,66,68-74, 76 in routes.py
        with self.client:
            # first login the user
            self.client.post(url_for('login'), data = dict(email = "admin@admin.com", password="admin2016"), follow_redirects = True)
            
            # then add a new post for the user
            response = self.client.post(
                '/post',
                data=dict(
                    title="Test Title",
                    content="Test Content"
                ),  # calls the /post page and insert the title and the content for a new post
                follow_redirects=True   # follows the redirecton
            )
            self.assertIn(b'Test Title', response.data) # Checks it the "Test Title" we posted is in the home page
    
    def test_about_page_view(self):
        # this tests that the abouit page can be
        # seen by anyone without the needs
        # to be logged in
        # test line 18 in routes.py
        response = self.client.get(url_for('about')) #calls the about page
        self.assertEqual(response.status_code, 200) #checks if it is accessible, code: 200
    
    def test_post_page_access_not_log(self):
        # this test that if a not logged-in
        # uset wants to access post
        # is sent to the login page
        # no chenges in statistics
        response = self.client.get(url_for('post')) #call the post page
        self.assertIn(b'login', response.data) # Checks if the we get the login page
    
    def test_post_page_access_logged(self):
        # this test that if a not logged-in
        # uset wants to access post
        # is sent to the login page
        # tests 37-39 in routes.py
        self.client.post(url_for('login'), data = dict(email = "admin@admin.com", password="admin2016"), follow_redirects = True)

        response = self.client.get(url_for('post')) #call the post page
        self.assertIn(b'Post', response.data) # Checks if get the post page
    
    def test_register(self):
        # this test checks if is possible to 
        # register as new user
        # tests 43, 45-62 in routes.py
        with self.client:
            resp=self.client.post(url_for('register'),data = dict(first_name="domen", last_name="gagli", email="dddd@gmail.com", password="1234",confirm_password="1234"),follow_redirects = True)
            #self.assertRedirects(resp.data,url_for('login'))
            self.assertIn(b'Login Page', resp.data)

    def test_account(self):
        # test it the account page is loaded correctly
        # tests 91-93, 99-104 in routes.py
        # first login the user
        self.client.post(url_for('login'), data = dict(email = "admin@admin.com", password="admin2016"), follow_redirects = True)
        response = self.client.get(url_for('account'))
        self.assertIn(b'admin', response.data)

    def test_account_modification(self):
        # this tests if the once the account is modified
        # by changing the first
        # the user is redirected to the home page
        # and the new name appears in the homepage
        # TESTS 94-98 IN ROUTES.PY

        # first login the user
        self.client.post(url_for('login'), data = dict(email = "admin@admin.com", password="admin2016"), follow_redirects = True)
        with self.client:
            resp=self.client.post(url_for('account'), data = dict(first_name="domen", last_name="gagli", email="dddd@gmail.com"),follow_redirects = True)
            self.assertIn(b'domen', resp.data)
    
    def test_logout(self):
        # this tests if after logged out
        # a the user is redirect to the login page
        # tests 84-85 in routes.py
        self.client.post(url_for('login'), data = dict(email = "admin@admin.com", password="admin2016"), follow_redirects = True)
        rv = self.client.get('logout',follow_redirects=True)
        self.assertIn(b'Login Page', rv.data)
    
    def test_account_delete(self):
        # tests the successful 
        # account deletion
        # tests 110-115, 117-121 in routes.py
        self.client.post(url_for('login'), data = dict(email = "admin@admin.com", password="admin2016"), follow_redirects = True)
        rv = self.client.get('account/delete',follow_redirects=True)
        self.assertIn(b'Register Page', rv.data)

