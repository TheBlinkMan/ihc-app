import unittest
import json
from app import create_app, db
from app.models import Role, get_role_by_email, is_email_address_institutional
from app.models import is_email_address

class EmailRegexTestCase(unittest.TestCase):

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

    def test_institutional_regex_with_invalid_email(self):
        #(TODO) Add more test cases
        email = "name.lastname@example.com"
        self.assertFalse(is_email_address_institutional(email))

    def test_institutional_regex_with_valid_email(self):
        institutional_email = "name.lastname@ifb.edu.br"
        self.assertTrue(is_email_address_institutional(institutional_email))

    def test_email_regex_with_invalid_email(self):
        #(TODO) Add more test cases
        email = "name.lastname@example."
        self.assertFalse(is_email_address(email))

    def test_email_regex_with_valid_email(self):
        email = "name.lastname@gmail.edu.br"
        self.assertTrue(is_email_address(email))


    def test_role_assignment(self):
        student_role = Role.query.filter_by(name = 'Student').first()
        student_email = "name.lastname@estudante.ifb.edu.br"
        role = get_role_by_email(student_email)
        self.assertTrue(role.id == student_role.id)

        teacher_role = Role.query.filter_by(name = 'Teacher').first()
        teacher_email = "name.lastname@ifb.edu.br"
        role = get_role_by_email(teacher_email)
        self.assertTrue(role.id == teacher_role.id)

        not_institutional_email = "name.lastname@example.com.br"
        role = get_role_by_email(not_institutional_email)
        self.assertIsNone(role)
