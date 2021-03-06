"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        # sign up or create new user

        u1 = User.signup("user_test_1", 'ut1@gmail.com', '12345', None)

        u2 = User.signup('user_test_2', 'ut2@gmail.com', '54321', None)

        db.session.add_all([u1, u2])
        db.session.commit()

        u1 = User.query.filter(username='user_test_1').first()
        u2 = User.query.filter(username='user_tesst_2').first()

        # User.query.delete()
        # Message.query.delete()
        # Follows.query.delete()

        self.client = app.test_client()
    def tearDown(self):
        # I don't quite understand these methods?
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_following(self):
        self.u1.following.append(self.u2)
        self.assertEqual(len(self.u1.following), 1)
        
        self.assertEqual(self.u1.following[0].id, self.u2.id)
    
# Does the repr method work as expected?
# Does is_following successfully detect when user1 is following user2?

    def test_is_following(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        # could write something with helper function and "self.u1.following contains self.u2.id"

        self.assertFalse(self.u2.is_following(self.u1))
        self.assertTrue(self.u1.is_following(self.u2))
    


# Does is_following successfully detect when user1 is not following user2?
# Does is_followed_by successfully detect when user1 is followed by user2?
# Does is_followed_by successfully detect when user1 is not followed by user2?
    def test_is_followed_by(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u2.is_followed_by(self.u1))
        

# Does User.create successfully create a new user given valid credentials?

    def test_signup(self):
        u3 = User('test_user_3', 'TU3@gmail.com', '54321', None)
        db.session.add(u3)
        db.session.commit()

        

        u3 = User.query.filter(username='test_user_3').first()

        all_users = User.query.all()

        self.assertIn(u3, all_users)
    


# Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
    # def test_failed_signup(self):
    #     # isn't the whole point of validating the input data of the form to prevent this?
    #     bad_user = User('', 'h.gmail.com', '12345')
    #     db.session.add(bad_user)



# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?