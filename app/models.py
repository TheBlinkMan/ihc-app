import re
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import current_user, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from .exceptions import ValidationError
from datetime import datetime
from werkzeug.utils import secure_filename
from .file_utility import allowed_file
from .validators import is_email_address
from .validators import is_email_address_institutional
from .validators import is_email_address_student
from .validators import is_teacher_email

def get_role_by_email(email):
    if is_email_address_student(email):
        return Role.query.filter_by(name = 'Student').first()
    #(TODO)
    #Add here a string test to give the administrator role to the right emails
    elif is_teacher_email(email):
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
    images = db.relationship('Image', backref = 'uploaded_by', lazy = 'dynamic')
    vles = db.relationship('VirtualLearningEnvironment', backref = 'author', lazy = 'dynamic')
    news = db.relationship('News', backref = 'author', lazy = 'dynamic')
    documents = db.relationship('Document', backref = 'uploaded_by', lazy = 'dynamic')
    opportunities = db.relationship('Opportunity', backref = 'author', lazy = 'dynamic')

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

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        return True

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
        if (name == '' or email == '' or password == '' or
           name is None or email is None or password is None):
            raise ValidationError('Invalid parameters')
        user = User.query.filter_by(email = email).first()
        if user is not None:
            raise ValidationError('User already registered.')
        if not is_email_address_institutional(email):
            raise ValidationError('Email address is not institutional.')
        if len(name) < 3:
            raise ValidationError('Invalid parameters')
        if len(password) < 8:
            raise ValidationError('Invalid parameters')

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

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(128), nullable = False)
    alternate = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_modified = db.Column(db.DateTime(), default=datetime.utcnow)
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)

    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'))

    @staticmethod
    def from_json(image_json):
        filename = image_json.get('filename')
        alternate = image_json.get('alternate')
        if filename == '' or filename == None:
            raise ValidationError('File must have a name')
        filename = secure_filename(filename)
        if not allowed_file(filename):
            raise ValidationError('File must have the extensions: pdf, txt, jpg')
        # test if the filename is None or the empty string and generate random filename
        image = Image()
        image.filename = filename
        image.alternate = alternate
        return image

    def to_json(self):
        image_json = {
                'id' : self.id,
                'uri' : url_for('api.get_image', id = self.id, _external = True),
                'filename' : self.filename,
                'uploaded_by' : url_for('api.get_user', id = self.user_id, _external = True),
                'alternate' : self.alternate,
                'last_modified' : self.last_modified,
                'creation_date' : self.creation_date
        }
        return image_json

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(128), nullable = False)
    body = db.Column(db.Text, nullable = False)

    @staticmethod
    def from_json(message_json):
        name = message_json.get('name')
        last_name = message_json.get('last_name')
        body = message_json.get('body')
        email = message_json.get('email')

        # (TODO)Change to not operation using falsy values
        if (name == '' or name == None or
                last_name == '' or last_name == None or
                body == '' or body == None or
                email == '' or email == None):
            raise ValidationError('Invalid or missing parameters')
        if not is_email_address(email):
            raise ValidationError('Invalid email')
        message = Message()
        message.name = name
        message.last_name = last_name
        message.email = email
        message.body = body

        return message

    def to_json(self):
        image_json = {
                "id" : self.id,
                "uri" : url_for('api.get_message', id = self.id, _external = True),
                "name" : self.name,
                "last_name" : self.last_name,
                "email" : self.email,
                "body" : self.body
        }
        return image_json

class VirtualLearningEnvironment(db.Model):
    __tablename__ = 'vles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False)
    link = db.Column(db.String(256), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    last_modified = db.Column(db.DateTime(), default=datetime.utcnow)
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)

    @staticmethod
    def from_json(vle_json):
        name = vle_json.get('name')
        link = vle_json.get('link')

        if name == '' or name == None or link == '' or link == None:
            raise ValidationError('Invalid parameters')

        # (TODO)verify if the link is valid

        vle = VirtualLearningEnvironment()
        vle.name = name
        vle.link = link
        return vle

    def to_json(self):
        vle_json = {
                "id" : self.id,
                "uri" : url_for('api.get_vle', id = self.id, _external = True),
                "name" : self.name,
                "link" : self.link,
                "author": url_for('api.get_user', id = self.author_id, _external=True),
                "last_modified" : self.last_modified,
                "creation_date" : self.creation_date
        }
        return vle_json

class Campus(db.Model):
    __tablename__ = 'campuses'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False)
    localization = db.Column(db.String(256), nullable = False)
    contacts = db.relationship('Contact', backref = 'campus', lazy = 'dynamic')

    @staticmethod
    def from_json(campus_json):
        name = campus_json.get('name')
        localization = campus_json.get('localization')

        if name == '' or name == None:
            raise ValidationError('Invalid arguments or parameters')

        campus = Campus()

        campus.name = name
        campus.localization = localization

        return campus

    def to_json(self):
        campus_json = {
                "id" : self.id,
                "uri" : url_for('api.get_campus', id=self.id, _external = True),
                "contacts" : url_for('api.get_campus_contacts', id=self.id, _external = True),
                "name" : self.name,
                "localization" : self.localization
        }

        return campus_json

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(128), nullable = False)
    telephone_number = db.Column(db.String(64))
    email = db.Column(db.String(128))
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id')) 

    @staticmethod
    def from_json(contact_json):
        description = contact_json.get('description')
        telephone_number = contact_json.get('telephone_number')
        email = contact_json.get('email')

        if (description == '' or description == None or
            telephone_number == '' or telephone_number == None):
            raise ValidationError('Invalid arguments or parameters')

        # (TODO) validate telephone number
        if email != None and email != '' and not is_email_address(email):
            raise ValidationError('Invalid email')

        contact = Contact()
        contact.description = description
        contact.telephone_number = telephone_number
        contact.email = email

        return contact

    def to_json(self):
        contact_json = {
                "id" : self.id,
                "uri" : url_for('api.get_contact', id=self.id, _external=True),
                "description" : self.description,
                "telephone_number" : self.telephone_number,
                "email" : self.email,
                "campus" : url_for('api.get_campus', id=self.campus_id, _external=True)
        }
        return contact_json

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key = True) 
    title = db.Column(db.String(256), nullable = False)
    link = db.Column(db.String(256))
    body = db.Column(db.Text)
    published = db.Column(db.Boolean, default = False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id')) 

    images = db.relationship('Image', backref='news', lazy = 'dynamic')

    @staticmethod
    def from_json(news_json):
        title = news_json.get('title')
        link = news_json.get('link')
        body = news_json.get('body')

        if title == '' or title == None:
            raise ValidationError('Invalid parameters or arguments')

        # Validation

        news = News()
        news.title = title
        news.link = link
        news.body = body

        return news

    def to_json(self):
        news_json = {
                "id" : self.id,
                "uri" : url_for('api.get_news_item', id=self.id, _external=True),
                "title" : self.title,
                "link" : self.link,
                "body" : self.body,
                "published" : self.published,
                "author" : url_for('api.get_user', id=self.author_id, _external=True),
                "images" : url_for('api.get_news_item_images', id=self.id, _external = True)
        }

        return news_json

class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable = False)
    description = db.Column(db.Text)

    courses = db.relationship('Course', backref='program', lazy='dynamic')

    @staticmethod
    def from_json(program_json):
        name = program_json.get('name')
        description = program_json.get('description')

        # Validation

        program = Program()
        program.name = name
        program.description = description

        return program

    def to_json(self):
        program_json = {
                "id" : self.id,
                "uri" : url_for('api.get_course', id=self.id, _external=True),
                "name" : self.name,
                "description" : self.description
        }

        return program_json

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable = False)
    class_hours = db.Column(db.Integer)
    weekly_meetings = db.Column(db.Integer)
    term_load = db.Column(db.Integer)
    term = db.Column(db.Integer)
    acronym = db.Column(db.String(10))

    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    documents = db.relationship('Document', backref='course', lazy='dynamic')

    @staticmethod
    def from_json(course_json):
        name = course_json.get('name')
        class_hours = course_json.get('class_hours')
        weekly_meetings = course_json.get('weekly_meetings')
        term_load = course_json.get('term_load')
        term = course_json.get('term')
        acronym = course_json.get('acronym')

        # Validate

        course = Course()
        course.name = name
        course.class_hours = class_hours
        course.weekly_meetings = weekly_meetings
        course.term_load = term_load
        course.acronym = acronym
        course.term = term

        return course

    def to_json(self):
        course_json = {
                "id" : self.id,
                "uri" : url_for('api.get_course', id = self.id, _external = True),
                "name" : self.name,
                "class_hours" : self.class_hours,
                "weekly_meetings" : self.weekly_meetings,
                "term_load" : self.term_load,
                "term" : self.term,
                "acronym" : self.acronym,
                "program" : url_for('api.get_program', id=self.program_id, _external=True)
        }
        return course_json

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False)
    filename = db.Column(db.String(128), nullable = False)

    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_modified = db.Column(db.DateTime(), default=datetime.utcnow)
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    @staticmethod
    def from_json(image_json):
        name = image_json.get('name')
        filename = image_json.get('filename')

        if name == '' or name == None:
            raise ValidationError('File must have a descriptive name')

        if filename == '' or filename == None:
            raise ValidationError('File must have a name')

        filename = secure_filename(filename)

        if not allowed_file(filename):
            raise ValidationError('File must have the extensions: pdf, txt, jpg')

        # test if the filename is None or the empty string and generate random filename
        document = Document()
        document.name = name
        document.filename = filename
        return document

    def to_json(self):
        image_json = {
                'id' : self.id,
                'uri' : url_for('api.get_document', id = self.id, _external = True),
                'name' : self.name,
                'filename' : self.filename,
                'uploaded_by' : url_for('api.get_user', id = self.uploader_id, _external = True),
                'last_modified' : self.last_modified,
                'creation_date' : self.creation_date,
        }
        return image_json

class Opportunity(db.Model):
    __tablename__ = 'opportunities'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256), nullable = False)
    institution = db.Column(db.String(256), nullable = False)
    vacancies_amount = db.Column(db.Integer)
    published = db.Column(db.Boolean, default = False)
    link = db.Column(db.String(256))
    description = db.Column(db.Text)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    images = db.relationship('Image', backref='opportunity', lazy='dynamic')

    @staticmethod
    def from_json(opportunity_json):

        title = opportunity_json.get('title')
        institution = opportunity_json.get('institution')
        vacancies_amount = opportunity_json.get('vacancies_amount')
        link = opportunity_json.get('link')
        description = opportunity_json.get('description')


        if title == None or title == '':
            raise ValidationError('Invalid arguments or parameter')

        if institution == None or institution == '':
            raise ValidationError('Invalid arguments or parameter')


        # (TODO) Validate

        opportunity = Opportunity()
        opportunity.title = title
        opportunity.institution = institution
        opportunity.vacancies_amount = vacancies_amount
        opportunity.link = link
        opportunity.description = description

        return opportunity

    def to_json(self):
        opportunity_json = {
                "id" : self.id,
                "uri" : url_for('api.get_opportunity', id = self.id, _external = True),
                "title" : self.title,
                "institution" : self.institution,
                "vacancies_amount" : self.vacancies_amount,
                "link" : self.link,
                "description" : self.description,
                "published" : self.published,
                "images" : url_for('api.get_opportunity_images', id=self.id, _external=True),
                "author" : url_for('api.get_user', id=self.author_id, _external=True)
        }
        return opportunity_json
