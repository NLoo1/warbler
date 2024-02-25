"""Message view tests."""

import os
from unittest import TestCase
from datetime import datetime
from models import db, User, Message, Follows
from dotenv import load_dotenv

from app import app, CURR_USER_KEY, do_logout

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL_TEST', 'postgresql:///warbler_test'))
os.environ['FLASK_ENV'] = 'production'

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser", html)

    def test_show_following(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get(f"/users/{self.testuser.id}/following")
            self.assertEqual(resp.status_code, 200)

    def test_show_following_anon(self):
        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}/following")
            self.assertEqual(resp.status_code, 302)

    def test_users_followers(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get(f"/users/{self.testuser.id}/followers")
            self.assertEqual(resp.status_code, 200)  

    def test_users_followers_anon(self):
        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}/following")
            self.assertEqual(resp.status_code, 302)

    
    