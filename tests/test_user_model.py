import unittest
import json
from app import create_app, db
from app.models import User

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        user = User()
        user.password = 'simple'
        self.assertIsNotNone(user.password_hash)

    def test_no_password_getter(self):
        user = User()
        user.password = 'simple'
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User()
        user.password = 'simple'
        self.assertTrue(user.verify_password('simple'))
        self.assertFalse(user.verify_password('elpmis'))

    def test_password_salts_are_random(self):
        user1 = User()
        user2 = User()
        user1.password = 'simple'
        user2.password = 'simple'
        self.assertTrue(user1.password_hash != user2.password_hash)

    def test_to_json(self):
        user = User(email='john.doe@latte.au.au', password='simple')
        db.session.add(user)
        db.session.commit()
        json_user = user.to_json()
        expected_keys = ['url', 'name', 'email', 'lattes']
        self.assertEqual(sorted(json_user.keys()), sorted(expected_keys))
        self.assertTrue('api/v1.0/users/' in json_user['url'])
