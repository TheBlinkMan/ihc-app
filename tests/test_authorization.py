import unittest
import json
from app import create_app, db
from app.models import User, Role, Permission, get_role_by_email
from flask import url_for

class AuthorizationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.create_all()
        Role.insert_roles()
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

    def test_admin_permission_decorator_with_admin_permission(self):
        email = 'john.doe@ifb.edu.br'
        password = 'hardtoguessstring'
        user = User()
        user.name = 'John Doe'
        user.email = email
        user.lattes = 'http://lattes.au.au'
        user.password = password
        user.confirmed = True
        user.role =  Role.query.filter_by(name = 'Administrator').first()

        self.assertTrue(user.can(Permission.ADMINISTER))

        db.session.add(user)
        db.session.commit()

        with self.client:
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
                    url_for('api.admin_only'),
                    headers=self.get_headers(token)
            )
            self.assertTrue(response.status_code == 200)

    def test_admin_permission_decorator_without_admin_permission(self):
        email = 'john.doe@estudante.ifb.edu.br'
        password = 'hardtoguessstring'
        user = User()
        user.name = 'John Doe'
        user.email = email
        user.lattes = 'http://lattes.au.au'
        user.password = password
        user.confirmed = True
        user.role = get_role_by_email(email)

        self.assertFalse(user.can(Permission.ADMINISTER))

        db.session.add(user)
        db.session.commit()

        with self.client:
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
                    url_for('api.admin_only'),
                    headers=self.get_headers(token)
            )
            self.assertTrue(response.status_code == 403)
