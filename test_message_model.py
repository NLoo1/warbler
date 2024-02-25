"""Message model tests."""

import os
from unittest import TestCase
from datetime import datetime
from models import db, User, Message, Follows
from dotenv import load_dotenv

from app import app

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL_TEST', 'postgresql:///warbler_test'))
os.environ['FLASK_ENV'] = 'production'

db.drop_all()
db.create_all()


class MessageModelTestCase(TestCase):

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

    def test_message(self):
        user = User.query.filter_by(username='testuser').first()
        msg = Message(
            text="TestMessage",
            timestamp=datetime.utcnow(),
            user_id = user.id
        )
        db.session.add(msg)
        db.session.commit()

        msg = Message.query.first()

        self.assertEqual(msg.id,1)
        self.assertEqual(msg.text,'TestMessage')
        self.assertEqual(msg.user_id,user.id)

    def test_repr(self):
        user = User.query.filter_by(username='testuser').first()
        msg = Message(
            text="TestMessage",
            timestamp=datetime.utcnow(),
            user_id = user.id
        )
        db.session.add(msg)
        db.session.commit()

        msg = Message.query.first()

        self.assertEqual(msg.__repr__(), f'Message Message.id, user id Message.user_id')
