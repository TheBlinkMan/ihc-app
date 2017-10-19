from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import current_user, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from .exceptions import ValidationError

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    lattes = db.Column(db.String(256), unique=True, index=True)

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

    @staticmethod
    def from_json(json_user):
        name = json_user.get('name')
        email = json_user.get('email')
        password = json_user.get('password')
        lattes = json_user.get('lattes')
        if name == '' or email == '' or password == '':
            raise ValidationError('Invalid parameters')
        #Validade email with Felipe's funciton and decide the user role
        #This function will evaluate if the e-mail is a institutional email or not
        user = User.query.filter_by(email = email).first()
        if user is not None:
            raise ValidationError('User already registered.')
        u = User()
        u.name = name
        u.email = email
        u.password = password
        u.lattes = lattes
        return u

    def to_json(self):
        json_user = {
                'url': url_for('api.get_user', id=self.id, _external=True),
                'name': self.name,
                'email': self.email,
                'lattes': self.lattes
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.email

class AnonymousUser(AnonymousUserMixin):
    pass

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
