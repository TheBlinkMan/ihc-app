from threading import Thread
import base64

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def async_save_file(fullpath, file_string):
    with open(fullpath, 'wb') as file:
        file.write(base64.b64decode(file_string))

def save_file(fullpath, file_string):
    thr = Thread(target=async_save_file, args=[fullpath, file_string])
    thr.start()
    return thr
