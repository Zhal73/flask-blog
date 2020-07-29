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

    def test_homepage_view(self):
        # this tests if the homepage is accessible
        # by anyone, without the needs for a
        # user to be logged in

        response = self.client.get(url_for('home')) #call the home page
        self.assertEqual(response.status_code, 200) #checks it it is accessible. code : 200

    def test_add_new_post(self):
        # this tests that once a user posts a new post,
        # the user is then redirected to the home page
        # and the new post is visible
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
