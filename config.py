import os


DEBUG = True

# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(24)])

SECRET_KEY = "#d#JCqTTW\nilK\\7m\x0bp#\tj~#H"


# JSON
basedir = os.path.abspath(os.path.dirname(__file__))
# TODO ajouter les paths en paramètre
# json_clubs_path = "/clubs.json"
# json_competitions_path = "/competitions.json"
