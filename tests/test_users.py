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

    def login(self, email, password):
        return self.client.post(
                    url_for('api.login'),
                    headers=self.get_headers(''),
                    data=json.dumps({'email': email, 'password': password})
                )

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
            response = self.login(admin_email, admin_password)
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

    def test_get_user_with_admin_user(self):
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
            response = self.login(admin_email, admin_password)
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('token'))
            token = json_response['token']

            response = self.client.get(
                    url_for('api.get_user', id = user.id),
                    headers = self.get_headers(token))
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('id'))
            response_user_id = json_response.get('id')
            self.assertTrue(response_user_id == user.id)

    def test_get_user_with_same_id(self):
        # The authenticated user id and the request id are the same

        email = 'john.doe@estudante.ifb.edu.br'
        password = 'hardtoguessstring'
        user = User()
        user.name = 'John Doe'
        user.email = email
        user.password = password
        user.lattes = 'https://lattes.au.au/johndoe'
        user.role = get_role_by_email(user.email)

        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.login(email, password)
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('token'))
            token = json_response['token']

            response = self.client.get(
                    url_for('api.get_user', id = user.id),
                    headers = self.get_headers(token))
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('id'))
            response_user_id = json_response.get('id')
            self.assertTrue(response_user_id == user.id)

    def test_create_user_with_blank_values(self):
        with self.client:
            response = self.client.post(
                    url_for('api.create_user'),
                    headers=self.get_headers(''),
                    data=json.dumps({'name' : '', 'email' : '', 'password' : ''}))
            self.assertTrue(response.status_code == 400)

            response = self.client.post(
                    url_for('api.create_user'),
                    headers=self.get_headers(''),
                    data=json.dumps({'name' : '', 'email' : 'john.doe@ifb.edu.br', 'password' : 'john12356'}))
            self.assertTrue(response.status_code == 400)

            response = self.client.post(
                    url_for('api.create_user'),
                    headers=self.get_headers(''),
                    data=json.dumps({'name' : 'John Doe', 'email' : 'john.doe@ifb.edu.br', 'password' : ''}))
            self.assertTrue(response.status_code == 400)

            response = self.client.post(
                    url_for('api.create_user'),
                    headers=self.get_headers(''),
                    data=json.dumps({'name' : 'John Doe', 'email' : '', 'password' : 'john123456'}))
            self.assertTrue(response.status_code == 400)

    def test_create_user_with_registered_email(self):
        name = 'John Doe'
        email = 'john.doe@estudante.ifb.edu.br'
        password = 'hardtoguessstring'
        user = User()
        user.name = name
        user.email = email
        user.password = password
        user.lattes = 'https://lattes.au.au/johndoe'
        user.role = get_role_by_email(user.email)

        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.post(
                    url_for('api.create_user'),
                    headers=self.get_headers(''),
                    data=json.dumps({'name' : 'Something', 'email' : email, 'password' : 'john123456'}))
            self.assertTrue(response.status_code == 400)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('message'))

    def test_create_user_without_intitutional_email(self):
        name = 'John Doe'
        email = 'john.doe@example.com'
        password = 'john123456'

        with self.client:
            response = self.client.post(
                    url_for('api.create_user'),
                    headers=self.get_headers(''),
                    data=json.dumps({'name' : name, 'email' : email, 'password' : password}))
            self.assertTrue(response.status_code == 400)

    def test_create_user_with_valid_parameters(self):
        name = 'John Doe'
        email = 'john.doe@estudante.ifb.edu.br'
        password = 'john123456'

        with self.client:
            response = self.client.post(
                    url_for('api.create_user'),
                    headers=self.get_headers(''),
                    data=json.dumps({'name' : name, 'email' : email, 'password' : password}))
            self.assertTrue(response.status_code == 201)

    def test_update_user_with_valid_input(self):
        name = 'John Doe'
        email = 'john.doe@estudante.ifb.edu.br'
        password = 'hardtoguessstring'
        lattes = 'https://lattes.au.au/johndoe'

        user = User()
        user.name = name
        user.email = email
        user.password = password
        user.lattes = lattes
        user.role = Role.query.filter_by(name = 'Student').first()

        db.session.add(user)
        db.session.commit()

        self.assertFalse(user.confirmed)

        confirmation_token = user.generate_confirmation_token()
        confirmation_token_ascii = confirmation_token.decode('ascii')

        response = self.login(email, password)
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('token'))
        authentication_token = json_response['token']

        with self.client:
            response = self.client.put(
                    url_for('api.update_user', id = user.id),
                    headers=self.get_headers(authentication_token),
                    data=json.dumps({'confirm' : confirmation_token_ascii})
            )
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('confirmed'))
            self.assertTrue(json_response.get('confirmed'))
            self.assertTrue(user.confirmed)

            new_name = 'John Dow'

            response = self.client.put(
                    url_for('api.update_user', id = user.id),
                    headers=self.get_headers(authentication_token),
                    data=json.dumps({'name' : new_name})
            )
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('name'))
            self.assertTrue(json_response.get('name') != name)
            self.assertTrue(user.name == new_name)

            new_lattes = 'https://lattes.au.au/johndow'

            response = self.client.put(
                    url_for('api.update_user', id = user.id),
                    headers=self.get_headers(authentication_token),
                    data=json.dumps({'lattes' : new_lattes})
            )
            self.assertTrue(response.status_code == 200)
            json_response = json.loads(response.data.decode('utf-8'))
            self.assertIsNotNone(json_response.get('lattes'))
            self.assertTrue(json_response.get('lattes') != lattes)
            self.assertTrue(user.lattes == new_lattes)
