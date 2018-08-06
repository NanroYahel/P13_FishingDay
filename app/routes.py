from flask import render_template, request
from app import app

import config as conf

from app import utils
from app.forms import LocationForm

@app.route('/')
@app.route("/index")
def index():
	"""Main page"""
	form = LocationForm()
	return render_template('index.html', form=form)


@app.route('/result', methods=['POST'])
def result():
	"""View used to display result of the users search"""
	city = request.form['location']
	meteo_data = utils.get_meteo_for_city(city)
	return render_template('result.html', meteo=meteo_data, city=city)

@app.route('/about')
def about():
	"""Display information about FishingDay project"""
	return render_template('about.html')

@app.route('/legal')
def legal():
	"""Display legal informations"""
	return render_template('legal.html')