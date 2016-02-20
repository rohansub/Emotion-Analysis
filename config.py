from os import path

# App details
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
DEBUG = True
SECRET_KEY = 'e3b54e9cf119f1a4fe31225e72c11919'

# Database details
SQLALCHEMY_DATABASE_URI = '{0}{1}'.format('sqlite:///',
                                          path.join(BASE_DIRECTORY, 'app.db'))
