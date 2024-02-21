"""Message view tests."""

import os
from unittest import TestCase
from datetime import datetime
from models import db, User, Message, Follows
from dotenv import load_dotenv

from app import app, CURR_USER_KEY, do_logout, do_login

load_dotenv()

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"
os.environ['FLASK_ENV'] = 'production'

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
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
        
        self.testuser2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = self.client.get(f"/users/{self.testuser.id}/messages")
            self.assertEqual(resp.status_code, 200)

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")
    
    def test_add_message_anon(self):
        with self.client as c:

            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            # Make sure it redirects
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized', html)
    
    def test_add_message_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = '99999999'

            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("unauthorized", html)

    def test_delete_message(self):

        # First add message
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = self.client.get(f"/users/{self.testuser.id}/messages")
            self.assertEqual(resp.status_code, 200)

            resp = c.post("/messages/new", data={"text": "Hello"})
            self.assertEqual(resp.status_code, 302)
            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

        # Now delete message
            
            resp = self.client.post(f"/messages/{msg.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Deleted', html)

    def test_delete_message_anon(self):
        # First add message
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = self.client.get(f"/users/{self.testuser.id}/messages")
            self.assertEqual(resp.status_code, 200)

            resp = c.post("/messages/new", data={"text": "Hello"})

            self.assertEqual(resp.status_code, 302)
            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

        # Now try to delete as anon
            with c.session_transaction() as sess:
                sess.clear()
                do_logout()

            resp = self.client.post(f"/messages/{msg.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn('unauthorized', html)

    def test_delete_message_logged_in(self):
        # First add message
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = self.client.get(f"/users/{self.testuser.id}/messages")
            self.assertEqual(resp.status_code, 200)
            resp = c.post("/messages/new", data={"text": "Hello"})
            self.assertEqual(resp.status_code, 302)
            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

        # Try to delete as another user
            
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = '999999999'

            resp = self.client.post(f"/messages/{msg.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn('unauthorized', html)


    def test_messages_show(self):
        # First add message
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = self.client.get(f"/users/{self.testuser.id}/messages")
            self.assertEqual(resp.status_code, 200)

            resp = c.post("/messages/new", data={"text": "Hello"})
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

        # Now check for message
            
            with c.session_transaction() as sess:
                sess.clear()
                do_logout()

            resp = self.client.get(f"/messages/{msg.id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hello", html)