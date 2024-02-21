"""User model tests."""

import os
from unittest import TestCase

from models import db, User, Message, Follows
from dotenv import load_dotenv

from app import app

load_dotenv()

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"
os.environ['FLASK_ENV'] = 'production'

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        User.signup(username=u1.username, email=u1.email,password=u1.password,image_url=u1.image_url)
        User.signup(username=u2.username, email=u2.email,password=u2.password,image_url=u2.image_url)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.drop_all()


    def test_user_model(self):
        """Does basic model work?"""

        user = User.query.get(1)

        # User should have no messages & no followers
        self.assertEqual(len(user.messages), 0)
        self.assertEqual(len(user.followers), 0)

    def test_is_following_u2(self):

        user = User.query.get(1)
        # user2 = User.query.get(2)

        # u1_u2 = Follows(user_being_followed_id=user2.id, user_following_id=user.id)
        # db.session.add(u1_u2)
        # db.session.commit()

        self.assertEqual(user.is_following(user), True)
    
    # def test_is_following_u1(self):
    #     u2_u1 = Follows(user_being_followed_id=1, user_following_id=2)
    #     db.session.add(u2_u1)
    #     db.session.commit()

    #     user = User.query.get(1)
    #     user2 = User.query.filter(id=2).first()
    #     self.assertEqual(user.is_following(user), True)

    # def test_is_not_following_u1(self):
    #     user = User.query.get(1)
    #     user2 = User.query.filter(id=2).first()
    #     self.assertEqual(user2.is_following(user), False)

    # def test_is_not_following_u2(self):
    #     user = User.query.get(1)
    #     user2 = User.query.filter(id=2).first()
    #     self.assertEqual(user.is_following(user2), False)

    # def test_signup(self):
    #     user = User(username="Test3", email="Test3@test.com", password="TestPwd3")
    #     self.assertEqual(user.signup, user)

    # def test_signup_fail(self):
    #     user = User(username="testuser", email="Test3@test.com", password="TestPwd3")
    #     self.assertNotEqual(user.signup, user)

    # def test_authenticate(self):
    #     user = User.query.get(1)
    #     authed_user = user.authenticate(user.username,user.password)
    #     self.assertEqual(authed_user, user)

    # def test_authenticate_username_fail(self):
    #     user = User.query.get(1)
    #     self.assertEqual(user.authenticate("Hello World!", user.password), False)

    # def test_authenticate_password_fail(self):
    #     user = User.query.get(1)
    #     print(user)
    #     self.assertEqual(user.authenticate(user.username, "bad password"), False)

    



