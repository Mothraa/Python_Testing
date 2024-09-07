import os


DEBUG = True

# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(24)])

SECRET_KEY = "#d#JCqTTW\nilK\\7m\x0bp#\tj~#H"


# JSON
basedir = os.path.abspath(os.path.dirname(__file__))