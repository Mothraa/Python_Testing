from flask import Flask,render_template,request,redirect,flash,url_for

from services import load_club_data, load_competition_data


# # moved to services.py
# def loadClubs():
#     with open('clubs.json') as c:
#          listOfClubs = json.load(c)['clubs']
#          return listOfClubs

# def loadCompetitions():
#     with open('competitions.json') as comps:
#          listOfCompetitions = json.load(comps)['competitions']
#          return listOfCompetitions


# app = Flask(__name__)
# # moved to config.py
# app.secret_key = 'something_special'

# TODO : move json load to __init__
competitions = load_competition_data()
clubs = load_club_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
