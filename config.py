import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(24)])

SECRET_KEY = os.getenv('SECRET_KEY')
# DATABASE_URL = os.getenv('DATABASE_URL')

# JSON
JSON_CLUBS_PATH = os.path.join(basedir, 'clubs.json')
JSON_COMPETITIONS_PATH = os.path.join(basedir, 'competitions.json')
JSON_BOOKINGS_PATH = os.path.join(basedir, 'bookings.json')

# maximum places allowed to reserve by competition per club
MAX_PLACES = 12
