from flask import Blueprint, render_template, request, redirect, flash, url_for, g

bp = Blueprint('main', __name__)

# TODO : regarder url_for qui est chargé pour le logout => a priori pour pointer sur un path lors de redirection
# TODO : authentification au lieu d'une simple identification, CSRF token, Flask-Login pour les permissions,...
# autres aspects sécurité ?


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/showSummary', methods=['POST'])
def showSummary():
    club_by_email_list = [club for club in g.clubs if club['email'] == request.form['email']]

    if len(club_by_email_list) == 0:
        flash("Email not found")
        print("DEBUG")
        return redirect(url_for('main.index'))

    if len(club_by_email_list) > 1:
        flash("Email found for {len(clubs_by_email)} clubs. Please contact administrator.")
        return redirect(url_for('main.index'))

    # cas nominal d'un seul club trouvé pour une adresse
    club = club_by_email_list[0]
    return render_template('welcome.html', club=club, competitions=g.competitions)


@bp.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in g.clubs if c['name'] == club][0]
    foundCompetition = [c for c in g.competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=g.competitions)


@bp.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in g.competitions if c['name'] == request.form['competition']][0]
    club = [c for c in g.clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=g.competitions)


# TODO: Add route for points display


@bp.route('/logout')
def logout():
    return redirect(url_for('main.index'))
