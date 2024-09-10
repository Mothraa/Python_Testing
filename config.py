import os

from dotenv import load_dotenv


DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(24)])

SECRET_KEY = os.getenv('SECRET_KEY')
# DATABASE_URL = os.getenv('DATABASE_URL')

# JSON

# TODO : paths a déplacer dans .env ? en prod ?
json_clubs_path = os.path.join(basedir, 'clubs.json')
json_competitions_path = os.path.join(basedir, 'competitions.json')
