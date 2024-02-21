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
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        user = User.query.filter_by(username="testuser").first()

        # User should have no messages & no followers
        self.assertEqual(len(user.messages), 0)
        self.assertEqual(len(user.followers), 0)

    def test_is_following_u2(self):

        user = User.query.filter_by(username="testuser").first()
        user2 = User.query.filter_by(username="testuser2").first()

        u1_u2 = Follows(user_being_followed_id=user2.id, user_following_id=user.id)
        db.session.add(u1_u2)
        db.session.commit()

        self.assertEqual(user.is_following(user2), True)
    
    def test_is_following_u1(self):

        user = User.query.filter_by(username="testuser").first()
        user2 = User.query.filter_by(username="testuser2").first()

        u2_u1 = Follows(user_being_followed_id=user.id, user_following_id=user2.id)
        db.session.add(u2_u1)
        db.session.commit()

        self.assertEqual(user2.is_following(user), True)

    def test_is_not_following_u1(self):
        user = User.query.filter_by(username="testuser").first()
        user2 = User.query.filter_by(username="testuser2").first()
        self.assertEqual(user2.is_following(user), False)

    def test_is_not_following_u2(self):
        user = User.query.filter_by(username="testuser").first()
        user2 = User.query.filter_by(username="testuser2").first()
        self.assertEqual(user.is_following(user2), False)

    def test_signup(self):
        user = User(username="Test3", email="Test3@test.com", password="TestPwd3",image_url=None)
        self.assertIsInstance(User.signup(username=user.username,email=user.email,password=user.password, image_url=user.image_url), User)

    def test_signup_fail(self):
        user = User(username="testuser", email="Test3@test.com", password="TestPwd3",image_url=None)
        self.assertNotIsInstance(User.signup(username=user.username,email=user.email,password=user.password, image_url=user.image_url), User)

    def test_authenticate(self):
        user = User.query.filter_by(username="testuser").first()
        authed_user = User.authenticate(user.username,"HASHED_PASSWORD")
        self.assertEqual(authed_user, user)

    def test_authenticate_username_fail(self):
        user = User.query.filter_by(username="testuser").first()
        self.assertEqual(user.authenticate("Hello World!", user.password), False)

    def test_authenticate_password_fail(self):
        user = User.query.filter_by(username="testuser").first()
        self.assertEqual(user.authenticate(user.username, "bad password"), False)

    



