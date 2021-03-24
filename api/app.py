#!/usr/bin/python3

# imports the require libraries
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

# Create endpoints for the api tempo

# app will be the instance of Flask
app = Flask(__name__)
# Call the CORS libarry of Flask
CORS(app)
# To manage session we use a secret key (random)
app.secret_key = os.urandom(16)
# login_manager contains all methods of the class LoginManager
login_manager = LoginManager()
# starts the LoginManager in this app Flask
login_manager.init_app(app)
# By default the view if a user is not login will be the login
login_manager.login_view = 'login'


def json_shows(shows):
    # This function gets the shows as objects(artists, venues, shows)
    # and returns a list of them
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
    # this function gets all information about organizer
    #  and the shows of this organizer
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
    # This function filter shows by date
    # the shows for the next month
    filter_shows = []
    today_str = datetime.date.today().isoformat()
    today = datetime.datetime.strptime(today_str, "%Y-%m-%d")
    seven_days = today + datetime.timedelta(days=7)
    fifteen_days = today + datetime.timedelta(days=15)
    one_month = today + datetime.timedelta(days=30)
    three_month = today + datetime.timedelta(days=90)
    if dates == "Próximo mes":
        for show in shows:
            if show.to_dict()["date"] >= today and show.to_dict()["date"] <= one_month:
                filter_shows.append(show)
    return filter_shows


@login_manager.user_loader
def load_user(user_id):
    # this function gets the id user that has an active session
    return storage.session.query(Organizer).get(user_id)


@app.before_request
def before():
    # This function verifies the session before a request
    # with the key userId (user id that has an active session)
    if "userId" in session:
        g.user = session["userId"]
    else:
        g.user = None


@app.after_request
def after(response):
    # This function verifies the session after a request
    # and gives the CORS with the frontend
    # allows the conncetion between the back and the front
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return(response)


@app.route("/login", methods=['POST'], strict_slashes=False)
def login():
    # This end-point validate the email and password of an user for
    # has a login successful, then finds the organizer by email
    # if this is not found returns a json
    # wiht status : “Email not found”  and a code http 404.
    # In the next step, we use the function check_password_hash()
    # That compares the password in the login wiht the registered
    # in the DB that is encrypted with MD5, if the function fails
    # returns a json  with status: “Invalid password” and a code http 401,
    # and another way if was successful returns a json with status: “OK”
    #  and a code http 200.
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
    # In this endpoint we create a new user of Organizer
    # First this function validates if the email sent by the new organizer
    # it's already in use by other organizer, in this case returns a json with
    # status: “Email existent” and a code http 409, otherwise a new organizer
    # is created with the data sent in the request form and returns a json with
    # status: “OK” and a code http 200.
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


@app.route("/profile", methods=['GET', 'POST'], strict_slashes=False)
def profile():
    # This function gets a cookie and pass as argument
    # in the function profile_json that have all information about
    # of an organizer  ans returns a json with this information
    user_id = request.cookies.get('userID')
    info_organizer = profile_json(user_id)
    info_org = info_organizer["organizador"][0]
    return jsonify(info_organizer)


@app.route("/shows", methods=['GET'], strict_slashes=False)
def shows():
    # gets all shows using the function json_shows
    # and finally returns  ajson with status code http 200
    shows = storage.session.query(Show).all()
    listShows = json_shows(shows)
    return jsonify(listShows), 200


@app.route("/", methods=["GET"])
def index():
    # this function gets the shows of the next month and
    # if the method http is GET returns a json wiht these shows
    # and a status code http 200, otherwise returns a json with
    # status: "method not allowed" and code http 405
    if request.method == "GET":
        all_shows = storage.session.query(Show).all()
        filter_shows = filter_by_date(all_shows, "Próximo mes")
        shows = json_shows(filter_shows)
        return jsonify(shows), 200
    return jsonify({"status": "metodo no permitido"}), 405


@app.route('/create-show', methods=['POST'])
def create_show():
    # This function takes the information
    # of the show. venue, artist and then
    # do a request wiht the cookie of the userId and
    # finally we create each object associated with this cookie or
    # organizer id, and all this if the request method is equal to POST
    if request.method == 'POST':
        show_attributes = ["description_show",
                           "price_ticket", "name_show", "hour", "date"]
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
        organizer = storage.session.query(
            Organizer).filter_by(id=user_id).first()
        city = storage.session.query(City).filter_by(
            city_name=venue_data["city"]).first()
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
    # app.run() is a method that allows start
    # our development server in the port: 5000
    # and host: *
    app.run(host="0.0.0.0", port=5000, debug=True)
