import unittest
import json
import time
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

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

    def test_valid_confirmation_token(self):
        user = User()
        user.name = 'John Doe'
        user.email = 'john.doe@ifb.edu.br'
        user.password = 'johndoe123'
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        self.assertTrue(user.confirm(token))

    def test_invalid_confirmation_token(self):
        user1 = User()
        user1.name  = 'John Doe'
        user1.email = 'john.doe@ifb.edu.br'
        user1.password = 'johndoe123'

        user2 = User()
        user2.name  = 'Jane Doe'
        user2.email = 'jane.doe@ifb.edu.br'
        user2.password = 'janedoe123'

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        token = user1.generate_confirmation_token()
        self.assertFalse(user2.confirm(token))

    def test_expired_confirmation_token(self):
        user = User()
        user.name  = 'John Doe'
        user.email = 'john.doe@ifb.edu.br'
        user.password = 'johndoe123'

        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token(1)

        time.sleep(2)

        self.assertFalse(user.confirm(token))

    def test_to_json(self):
        #get a random role so the method to_json can be called without raising
        # an exception.
        role = Role.query.first()
        user = User(email='john.doe@latte.au.au', password='simple', role=role)
        db.session.add(user)
        db.session.commit()
        json_user = user.to_json()
        expected_keys = ['uri', 'id', 'name', 'email', 'lattes', 'confirmed', 'role']
        self.assertEqual(sorted(json_user.keys()), sorted(expected_keys))
        self.assertTrue('api/v1.0/users/' in json_user['uri'])

    def test_permissions(self):
        user = User()
        user.role = Role.query.filter_by(name = 'Student').first()
        self.assertTrue(user.can(Permission.WRITE_CONTENT))
        self.assertFalse(user.can(Permission.REVIEW_CONTENT))
        self.assertFalse(user.can(Permission.PUBLISH_CONTENT))
        self.assertFalse(user.is_administrator())

        user.role = Role.query.filter_by(name = 'Teacher').first()
        self.assertTrue(user.can(Permission.WRITE_CONTENT |
                              Permission.REVIEW_CONTENT |
                              Permission.PUBLISH_CONTENT))
        self.assertFalse(user.is_administrator())

        user.role = Role.query.filter_by(name = 'Administrator').first()
        self.assertTrue(user.can(Permission.WRITE_CONTENT |
                              Permission.REVIEW_CONTENT |
                              Permission.PUBLISH_CONTENT))
        self.assertTrue(user.is_administrator())

    def test_anonymous_user_permissions(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.WRITE_CONTENT))
        self.assertFalse(user.can(Permission.REVIEW_CONTENT))
        self.assertFalse(user.can(Permission.PUBLISH_CONTENT))
        self.assertFalse(user.is_administrator())
