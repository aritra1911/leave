import os
from secrets import *

# Enable the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Define the database - PostgreSQL
SQLALCHEMY_DATABASE_URI = '{0}+{1}://{2}:{3}@{4}:{5}/{6}'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)
DATABASE_CONNECT_OPTIONS = {}

SQLALCHEMY_TRACK_MODIFICATIONS = False


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2


# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
