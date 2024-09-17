from flask import Blueprint, render_template, request, redirect, flash, url_for, g

from .services import BookingService

bp = Blueprint('main', __name__)

# TODO : regarder url_for qui est chargé pour le logout => a priori pour pointer sur un path lors de redirection
# TODO : authentification au lieu d'une simple identification, session flask, CSRF token (flask-WTF),
# TODO : Flask-Login pour les permissions,... autres aspects sécurité ?


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/showSummary', methods=['POST'])
def showSummary():
    club_by_email_list = [club for club in g.clubs if club['email'] == request.form['email']]
    # TODO : interdire la reservation de places pour des compétitions qui ont déjà eu lieu

    if len(club_by_email_list) == 0:
        flash("Email not found")
        return redirect(url_for('main.index'))

    if len(club_by_email_list) > 1:
        flash(f"Email found for {len(club_by_email_list)} clubs. Please contact administrator.")
        return redirect(url_for('main.index'))

    # cas nominal d'un seul club trouvé pour une adresse
    club = club_by_email_list[0]
    return render_template('welcome.html', club=club, competitions=g.competitions)


@bp.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in g.clubs if c['name'] == club][0]
    foundCompetition = [c for c in g.competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=g.competitions)


@bp.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    booking_service = BookingService(g.clubs, g.competitions)

    club = booking_service.get_club_by_name(request.form['club'])
    competition = booking_service.get_competition_by_name(request.form['competition'])

    try:
        places_required = int(request.form.get('places', ''))
    except ValueError:
        flash('Invalid number of places')
        return render_template('welcome.html', club=club, competitions=g.competitions)

    # On vérifie que la competition a suffisamment de places
    if not booking_service.has_enough_places(competition, places_required):
        flash(f"Not enough places in competition ({competition['numberOfPlaces']}) to book {places_required} places.")
        return render_template('booking.html', club=club, competition=competition)

    # competition['numberOfPlaces'] = competition['numberOfPlaces'] - placesRequired

    # TODO update JSON file
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=g.competitions)


# TODO: Add route for points display


@bp.route('/logout')
def logout():
    flash("Logout!")
    return redirect(url_for('main.index'))
