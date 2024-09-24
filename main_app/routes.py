from flask import Blueprint, render_template, request, redirect, flash, url_for, g

from .services import BookingService, JSONSaverService, JSONLoaderService

bp = Blueprint('main', __name__)

# TODO : regarder url_for qui est chargé pour le logout => a priori pour pointer sur un path lors de redirection
# TODO : authentification au lieu d'une simple identification, session flask, CSRF token (flask-WTF),
# TODO : Flask-Login pour les permissions,... autres aspects sécurité ?


@bp.route('/')
def index():
    json_loader = JSONLoaderService()
    clubs = json_loader.get_clubs()
    return render_template('index.html', clubs=clubs)


@bp.route('/showSummary', methods=['POST'])
def showSummary():
    club_by_email_list = [club for club in g.clubs if club['email'] == request.form['email']]

    if not club_by_email_list:
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
    foundClub = next((c for c in g.clubs if c['name'] == club), None)
    foundCompetition = next((c for c in g.competitions if c['name'] == competition), None)

    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('main.index'))


@bp.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    booking_service = BookingService(g.clubs, g.competitions)
    save_service = JSONSaverService()
    load_service = JSONLoaderService()

    club = booking_service.get_club_by_name(request.form['club'])
    competition = booking_service.get_competition_by_name(request.form['competition'])

    # On vérifie que le nombre de place demandé est un nombre entier positif
    try:
        places_required = int(request.form.get('places', ''))
        if places_required <= 0:
            raise ValueError("Invalid number of places")
    except ValueError:
        flash('Invalid number of places')
        return render_template('welcome.html', club=club, competitions=g.competitions)

    # On vérifie si la compétition est dans le futur ou déjà passée
    if not booking_service.is_competition_in_future(competition):
        flash("Competition already past")
        return render_template('welcome.html', club=club, competitions=g.competitions)

    # On récupère les places que le club a déjà réservé pour cette compétition
    bookings = load_service.get_bookings()
    already_reserved_places = booking_service.get_reserved_places(bookings, club, competition)

    # On vérifie que le nombre de places demandées est inférieur a la limite authorisée par clubs\
    # cela correspond aux placées souhaitées + celles précédemment reservées.
    if not booking_service.is_ok_with_max_places_limit(places_required + already_reserved_places):
        flash(f"Not allowed to book {places_required} places.\
                You exceed the limit by competitions ({booking_service.max_places} places).")
        return render_template('booking.html', club=club, competition=competition)

    # On vérifie que la competition a suffisamment de places
    if not booking_service.has_enough_places(competition, places_required):
        flash(f"Not enough places in competition ({competition['numberOfPlaces']}) to book {places_required} places")
        return render_template('booking.html', club=club, competition=competition)

    # On vérifie que le club à suffisamment de places (points) par rapport a sa demande
    if not booking_service.has_enough_points(club, places_required):
        flash("Not enough points to book competition places")
        return render_template('booking.html', club=club, competition=competition)

    # On met à jour les places et les points
    competition['numberOfPlaces'] -= places_required
    club['points'] -= places_required

    # gestion des reservations (formatage des données avant sauvegarde)
    updated_bookings = booking_service.handle_bookings(club,
                                                       competition,
                                                       places_required,
                                                       bookings
                                                       )

    # sauvegarde des fichiers json
    # TODO : pb de sauvegarde asynchrone\
    # (erreur dans un des fichiers json => corruption des données ; sauvegarde concomitante,...)
    save_service.save_clubs(g.clubs)
    save_service.save_competitions(g.competitions)
    save_service.save_bookings(updated_bookings)

    flash('Great-booking complete!')
    # TODO faire une redirection 302 après soumission du formulaire
    return render_template('welcome.html', club=club, competitions=g.competitions)


@bp.route('/logout')
def logout():
    flash("Logout!")
    return redirect(url_for('main.index'))
