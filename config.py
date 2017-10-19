import os

WITH_PAGINATION = os.environ.get('WITH_PAGINATION', 1)
DEFAULT_RESULTS_PER_PAGE = 15
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sqlite.db')
