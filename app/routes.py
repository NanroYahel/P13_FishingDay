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


# 'GET' used for developpement - TO DELETE !!!!!!
@app.route('/result', methods=['POST', 'GET'])
def result():
	"""View used to display result of the users search"""
	if request.method == 'GET':
		city = 'test'
	else:
		city = request.form['location']
	meteo_data = utils.get_meteo_for_city(city)
	"""Page to display the result of the user search"""
	return render_template('result.html', meteo=meteo_data, city=city)