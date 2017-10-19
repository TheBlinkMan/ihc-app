import unittest
import json
from app import create_app, db
from flask import url_for

class UsersTestCase(unittest.TestCase):

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

    def get_headers(self, token):
        return {
                'Authorization' : 'Bearer ' + token,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
        }

    def test_users_create_user_with_blank_values(self):
        with self.client:
            response = self.client.post(
                    url_for('api.create_user'),
                    headers=self.get_headers(''),
                    data=json.dumps({'email' : '', 'password' : ''}))
            self.assertTrue(response.status_code == 400)
