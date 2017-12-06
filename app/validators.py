import re

INSTITUTIONAL_EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@(estudante\.)?ifb\.edu\.br$)")
STUDENT_EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@estudante\.ifb\.edu\.br$)")
TEACHER_EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@ifb\.edu\.br$)")
EMAIL_REGEX = re.compile(r"(^(([^<>()\[\]\\.,;:\s@]+(\.[^<>()\[\]\\.,;:\s@]+)*)|(.+))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$)")
TELEPHONE_NUMBER_REGEX = re.compile(r"(\(d{2}\)|d{2}) d{4,5}-?d{4}")

def is_email_address_institutional(email):
    if INSTITUTIONAL_EMAIL_REGEX.match(email): # will return True or None
        return True
    return False

def is_email_address(email):
    if EMAIL_REGEX.match(email): # will return True or None
        return True
    return False

def is_email_address_student(value):
    if STUDENT_EMAIL_REGEX.match(value):
        return True
    return False

def is_teacher_email(value):
    if TEACHER_EMAIL_REGEX.match(value):
        return True
    return False

def is_telephone_number(value):
    if TELEPHONE_NUMBER_REGEX.match(value):
        return True
    return False

def has_minimum_length(value, length):
    if len(value) >= length:
        return True
    return False

def is_string_present(value):
    if value != None and value != '':
        return True
    return False

def is_integer(value):
    if isinstance(value, int):
        return True
    return False
