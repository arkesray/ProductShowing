import os
from tempfile import mkdtemp

UPLOAD_FOLDER = os.path.abspath("") + "\\ProductShowing\\uploads"
SECRET_KEY = "hello"

SQLALCHEMY_DATABASE_URI = 'sqlite:///database/database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# configure session to use filesystem (instead of signed cookies)
SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

MAX_CONTENT_LENGTH = 1 * 1024 * 1024
