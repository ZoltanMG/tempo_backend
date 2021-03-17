#!/usr/bin/python3
from flask import Flask
from models.base_model import Base
from models.organizer import Organizer
from flask import render_template, jsonify, session, url_for, request, redirect, g, Response, make_response, send_file, json, flash
from flask_login import login_required, login_user, logout_user, LoginManager
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from models import storage
from models.city import City
from models.show import Show, ShowArtist
from models.venue import Venue
from models.artist import Artist
from models.organizer import Organizer
from models.social_organizer import SocialOrganizer
from models.artist import Artist
from pprint import pprint
from flask_cors import CORS
"""
Create endpoints for the api
"""

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(16)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

##### functions #####

def json_shows(shows):
    """
    ESTA FUNCION OBTIENE LOS SHOWS COMO OBJETOS(ARTISTAS, VENUES, SHOW) Y RETORNA UNA LISTA DE ELLOS
    """
    shows_finales = []
    show_unico = []
    for show in shows:
        show_unico.append(show.to_dict())
        show_unico.append([artist.to_dict() for artist in show.artists()])
        venue = storage.session.query(
            Venue).filter_by(id=show.venue_id).first()
        show_unico.append(venue.to_dict())
        shows_finales.append(show_unico)
        show_unico = []
    return shows_finales

def profile_json(user_id):
    organizer_dict = {}
    organizer = storage.session.query(Organizer).filter_by(id=user_id).first()
    copy_dict_organizer = organizer.to_dict().copy()
    if "pwd" in copy_dict_organizer:
        copy_dict_organizer.pop('pwd', None)
    organizer_dict["organizador"] = [copy_dict_organizer, [venue.to_dict()
                                                           for venue in organizer.venues]]
    organizer_dict["shows"] = json_shows(organizer.shows)
    return (organizer_dict)

def filter_by_date(shows, dates):
    # variable seven para almacenar el datetime para los rangos
    filter_shows = []
    today_str = datetime.date.today().isoformat()
    today = datetime.datetime.strptime(today_str, "%Y-%m-%d")
    seven_days = today + datetime.timedelta(days=7)
    fifteen_days = today + datetime.timedelta(days=15)
    one_month = today + datetime.timedelta(days=30)
    three_month = today + datetime.timedelta(days=90)
    if dates == "Hoy":
        for show in shows:
            if show.to_dict()["date"] == today:
                filter_shows.append(show)
    elif dates == "Próximos 7 días":
        for show in shows:
            if show.to_dict()["date"] >= today and show.to_dict()["date"] <= seven_days:
                filter_shows.append(show)
    elif dates == "próximos 15 días":
        for show in shows:
            if show.to_dict()["date"] >= today and show.to_dict()["date"] <= fifteen_days:
                filter_shows.append(show)
    elif dates == "Próximo mes":
        for show in shows:
            if show.to_dict()["date"] >= today and show.to_dict()["date"] <= one_month:
                filter_shows.append(show)
    elif dates == "próximos 3 meces":
        for show in shows:
            if show.to_dict()["date"] >= today and show.to_dict()["date"] <= three_month:
                filter_shows.append(show)
    elif dates == "Todos":
        for show in shows:
            filter_shows.append(show)
    return filter_shows

##### endpoints #####

@login_manager.user_loader
def load_user(user_id):
    return storage.session.query(Organizer).get(user_id)


@app.before_request
def before():
    if "userId" in session:
        g.user = session["userId"]
    else:
        g.user = None


@app.after_request
def after(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return(response)


@app.route("/login", methods=['POST'], strict_slashes=False)
def login():
    """
    Este end-point validan el correo y contraseña de un usuario para
    realizar un inicio de sesión exitoso.
    Se busca un organizer filtrandolo por email, si no lo encuentra retorna un
    json con estatus: “Email not found” y un código http 404.
    Siguiente a eso usamos la función  check_password_hash() que compara la
    contraseña ingresada con la registrada en la base de datos que está
    encriptada con MD5, sí la función falla retorna un json con
    status: “Invalid password” y un código http 401,
    de ser exitoso retorna un json con status: “OK” y un código http 200.
    """
    if request.method == "POST":
        user = storage.session.query(Organizer).filter_by(
            email=request.json['email']).first()
        if user is None:
            return jsonify({"status": "Email not found"}), 404
        if user and check_password_hash(user.pwd, request.json['pwd']):
            session["userEmail"] = user.email
            session["userId"] = user.id
            login_user(user)
            session.permanent = True
            resp = make_response(jsonify(user.to_dict()))
            resp.set_cookie('userID', user.id, httponly=True)
            return resp, 200
        return jsonify({"status": "Invalid password"}), 401
    return jsonify({"hp": "ererugf87eryg"})


@app.route("/register", methods=['POST'], strict_slashes=False)
def register():
    """
    En este end-point creamos un nuevo usuario de organizador.
    Primero se valida si el correo enviado por el nuevo organizador
    ya está en uso por otro organizador, de ser así se retorna un json con
    status: “Email existent” y un código http 409, de lo contrario se crea un
    nuevo organizador con los datos enviados en el formulario y se retorna un
    json con status: “OK” y un código http 200.
    """
    data_json = request.json
    user_email = storage.session.query(Organizer).filter_by(
        email=data_json['email']).first()

    if user_email is not None:
        return jsonify({"status": "Email existent"}), 409
    password = data_json['pwd']
    try:
        nameOrganizer = data_json['names_organizer']
    except:
        return jsonify({"status": "debes ingresar un nombre de organizador!"}), 400
    email = data_json['email']
    pwd = data_json['pwd']
    pwd_md5 = generate_password_hash(pwd)
    new_organizer = Organizer()
    data_organizer = data_json.copy()
    data_organizer["pwd"] = pwd_md5
    for key, value in data_organizer.items():
        setattr(new_organizer, key, value)
    new_organizer.save()
    return jsonify(data_organizer), 200


@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("login"))


@app.route("/profile", methods=['GET', 'POST'], strict_slashes=False)
def profile():
    user_id = request.cookies.get('userID')
    info_organizer = profile_json(user_id)
    info_org = info_organizer["organizador"][0]
    return jsonify(info_organizer)


@app.route("/change_pwd", methods=['GET', 'POST'], strict_slashes=False)
def change_pwd():
    orgId = session['userId']
    if request.method == 'POST':
        organizer = storage.session.query(
            Organizer).filter_by(id=orgId).first()
        if not check_password_hash(organizer.pwd, request.form['pwd']):
            flash('La contraseña actual es incorrecta.')
            return redirect(url_for('change_pwd'))
        if request.form['newPwd'] != request.form['confirmPwd']:
            flash('La nueva contraseña y su confirmación no coinciden.')
            return redirect(url_for('change_pwd'))
        organizer.pwd = generate_password_hash(request.form['newPwd'])
        organizer.save()
        flash('Cambio de contraseña exitoso.')
        return redirect(url_for("profile"))
    return render_template("change_pwd.html")


@app.route("/shows", methods=['GET'], strict_slashes=False)
def shows():
    shows = storage.session.query(Show).all()
    listShows = json_shows(shows)
    return jsonify(listShows), 200


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        all_shows = storage.session.query(Show).all()
        filter_shows = filter_by_date(all_shows, "Próximo mes")
        shows = json_shows(filter_shows)
        return jsonify(shows), 200
    return jsonify({"status": "metodo no permitido"}), 405


@app.route('/create-show', methods=['POST'])
def create_show():
    if request.method == 'POST':
        show_attributes = ["description_show", "price_ticket", "name_show", "hour", "date"]
        artist_attributes = ["genre_artist", "artist_name"]
        venue_attributes = ["venue_name", "address", "city", "description"]
        show_data = {}
        artist_data = {}
        venue_data = {}
        all_data = request.json['data']
        for key, value in all_data.items():
            if key in show_attributes:
                show_data[key] = value
            if key in artist_attributes:
                artist_data[key] = value
            if key in venue_attributes:
                 venue_data[key] = value
        user_id = request.cookies.get('userID')
        organizer = storage.session.query(Organizer).filter_by(id=user_id).first()
        city = storage.session.query(City).filter_by(city_name=venue_data["city"]).first()
        venue_data["city_id"] = city.id
        del venue_data["city"]
        venue = organizer.create_venue(venue_data)
        artist = organizer.create_artist(artist_data)
        date_str = show_data["date"]
        year = int(date_str[0:4])
        month = int(date_str[5:7])
        day = int(date_str[8:10])
        date = datetime.datetime(year, month, day, 0, 0, 0)
        show_data["date"] = date
        show_data["venue_id"] = venue.id
        show_data["status_show"] = "Confirmado"
        show = organizer.create_show(show_data)
        show_artist = ShowArtist(
            artist_id=artist.id,
            show_id=show.id
        )
        show_artist.save()
        return jsonify({"status": "OK"})
    return jsonify({"error": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
