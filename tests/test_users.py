import unittest
import json
from app import create_app, db
from flask import url_for
from app.models import User, Role, Permission, get_role_by_email

class UsersTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
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

    def test_users_create_user_with_blank_values(self):
        with self.client:
            response = self.client.post(
                    url_for('api.create_user'),
                    headers=self.get_headers(''),
                    data=json.dumps({'email' : '', 'password' : ''}))
            self.assertTrue(response.status_code == 400)

    def test_get_users(self):
        user = User()
        user.name = 'John Doe'
        user.email = 'john.doe@estudante.ifb.edu.br'
        user.password = 'hardtoguessstring'
        user.lattes = 'https://lattes.au.au/johndoe'
        user.role = get_role_by_email(user.email)

        user2 = User()
        user2.name = 'Jane Doe'
        user2.email = 'jane.doe@ifb.edu.br'
        user2.password = 'somestring'
        user2.lattes = 'https://lattes.au.au/janedoe'
        user2.role = get_role_by_email(user2.email)

        admin_email = 'admin@ifb.edu.br'
        admin_password = 'somestring'

        user3 = User()
        user3.name = 'Admin'
        user3.email = admin_email
        user3.password = admin_password
        user3.lattes = 'https://lattes.au.au/something'
        user3.role = Role.query.filter_by(name = 'Administrator').first()

        self.assertTrue(user3.can(Permission.ADMINISTER))

        db.session.add_all([user, user2, user3])
        db.session.commit()

        with self.client:
            response = self.client.post(
                    url_for('api.login'),
                    headers=self.get_headers(''),
                    data=json.dumps(
                        {'email': admin_email, 'password': admin_password})
            )
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('token'))
            token = json_response['token']

            response = self.client.get(
                    url_for('api.get_users'),
                    headers = self.get_headers(token))
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('users'))
