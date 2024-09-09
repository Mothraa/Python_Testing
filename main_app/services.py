import json

# lecture et enregistrement des json


# TODO : regrouper la lecture du json dans la meme classe ?
def load_club_data(filename='clubs.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data.get('clubs', [])
    except FileNotFoundError:
        raise Exception(f"Le fichier {filename} est introuvable")
    except json.JSONDecodeError:
        raise Exception(f"Erreur de décodage du fichier {filename}")


def load_competition_data(filename='competitions.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data.get('competitions', [])
    except FileNotFoundError:
        raise Exception(f"Le fichier {filename} est introuvable")
    except json.JSONDecodeError:
        raise Exception(f"Erreur de décodage du fichier {filename}")

# def load_competition_data():
#     with open('competitions.json') as f:
#         competitions_list = json.load(f)['competitions']
#     return competitions_list
