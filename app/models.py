import re
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import current_user, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from .exceptions import ValidationError

INSTITUTIONAL_EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[estudante\.]?ifb\.edu\.br$)")
STUDENT_EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@estudante\.ifb\.edu\.br$)")
TEACHER_EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@ifb\.edu\.br$)")
EMAIL_REGEX = re.compile(r"(^(([^<>()\[\]\\.,;:\s@]+(\.[^<>()\[\]\\.,;:\s@]+)*)|(.+))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$)")

def is_email_address_institutional(email):
    if INSTITUTIONAL_EMAIL_REGEX.match(email): # will return True or None
        return True
    return False

def is_email_address(email):
    if EMAIL_REGEX.match(email): # will return True or None
        return True
    return False

def get_role_by_email(email):
    if STUDENT_EMAIL_REGEX.match(email):
        return Role.query.filter_by(name = 'Student').first()
    #(TODO)
    #Add here a string test to give the administrator role to the right emails
    elif TEACHER_EMAIL_REGEX.match(email):
        return Role.query.filter_by(name = 'Teacher').first()
    else:
        return None

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    lattes = db.Column(db.String(256), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default = False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @staticmethod
    def from_json(json_user):
        name = json_user.get('name')
        email = json_user.get('email')
        password = json_user.get('password')
        lattes = json_user.get('lattes')
        if name == '' or email == '' or password == '':
            raise ValidationError('Invalid parameters')
        user = User.query.filter_by(email = email).first()
        if user is not None:
            raise ValidationError('User already registered.')
        if not is_email_address_institutional(email):
            raise ValidationError('Email address is not institutional.')
        u = User()
        u.role = get_role_by_email(email)
        u.name = name
        u.email = email
        u.password = password
        u.lattes = lattes
        return u

    def to_json(self):
        json_user = {
                'uri': url_for('api.get_user', id=self.id, _external=True),
                'id': self.id,
                'name': self.name,
                'email': self.email,
                'role': self.role.name,
                'confirmed': self.confirmed,
                'lattes': self.lattes
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.email

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    WRITE_CONTENT = 0x01 #create content
    REVIEW_CONTENT = 0x02 #Can review student's content
    PUBLISH_CONTENT = 0x04
    ADMINISTER = 0x80 #delete news and update user's accounts

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Student': Permission.WRITE_CONTENT,
            'Teacher': (Permission.WRITE_CONTENT |
                        Permission.REVIEW_CONTENT |
                        Permission.PUBLISH_CONTENT),
            'Administrator': 0xff
        }
        for r in roles:
            role =  Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name
