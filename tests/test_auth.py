import unittest
import json
from app import create_app, db
from app.models import User
from flask import url_for

class AuthTestCase(unittest.TestCase):

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

    def test_login_with_blank_credentials(self):
        # Test for get_news
        with self.client:
            response = self.client.post(
                    url_for('api.login'),
                    headers=self.get_headers(''),
                    data=json.dumps({'email': '', 'password': ''}))
            self.assertTrue(response.status_code == 400)

    def test_login_without_required_key_value_pair(self):
        with self.client:
            response = self.client.post(
                    url_for('api.login'),
                    headers=self.get_headers(''),
                    data=json.dumps({'password': ''})
            )
            self.assertTrue(response.status_code == 400)

    def test_login_with_invalid_user(self):
        email = 'imadeitup@late.au.au'
        password = 'johndoepassword'

        with self.client:
            response = self.client.post(
                    url_for('api.login'),
                    headers=self.get_headers(''),
                    data=json.dumps({'email': email, 'password': password})
            )
        self.assertTrue(response.status_code == 400)

    def test_login_with_valid_user(self):
        email = 'john.doe@something.com.zz'
        password = 'simple'
        user = User()
        user.name = 'John Doe'
        user.email = email 
        user.lattes = 'http://late.au.au'
        user.password = password

        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.post(
                    url_for('api.login'),
                    headers=self.get_headers(''),
                    data=json.dumps({'email': email, 'password': password})
            )
            self.assertTrue(response.status_code == 200)

    def test_login_with_wrong_password(self):
        email = 'john.doe2@something.com.zz'
        password = 'simple'
        user = User()
        user.name = 'John Doe 2'
        user.email = email 
        user.lattes = 'http://late.au.au'
        user.password = password

        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.post(
                    url_for('api.login'),
                    headers=self.get_headers(''),
                    data=json.dumps({'email': email, 'password': 'wrongpassword'})
            )
            self.assertTrue(response.status_code == 400)

    def test_token_authentication(self):
        email = 'john.doe3@something.com.zz'
        password = 'simple'
        user = User()
        user.name = 'John Doe 3'
        user.email = email
        user.lattes = 'http://late.au.au'
        user.password = password

        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.get(
                url_for('api.get_user', id=user.id),
                headers=self.get_headers('wrong-token'))
            self.assertTrue(response.status_code == 401)

            response = self.client.post(
                    url_for('api.login'),
                    headers=self.get_headers(''),
                    data=json.dumps({'email': email, 'password': password})
            )
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('token'))
            token = json_response['token']

            response = self.client.get(
                    url_for('api.get_user', id=user.id),
                    headers=self.get_headers(token)
            )
            self.assertTrue(response.status_code == 200)
