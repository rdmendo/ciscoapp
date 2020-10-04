from flask import render_template, url_for, flash, redirect, Response, session, request, Blueprint
from ciscoapp import app, db, bcrypt
from ciscoapp.models import AdvertisedNetwork

main = Blueprint('main', __name__)

@main.route("/",  methods=['GET', 'POST'])
def index():
    get_network = reversed(AdvertisedNetwork.query.order_by(AdvertisedNetwork.id).all()[-10:])
    return render_template('index.html', network=get_network)
