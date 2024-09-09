import json

# lecture et enregistrement des json


def load_club_data():
    with open('clubs.json') as f:
        clubs_list = json.load(f)['clubs']
    return clubs_list


def load_competition_data():
    with open('competitions.json') as f:
        competitions_list = json.load(f)['competitions']
    return competitions_list
