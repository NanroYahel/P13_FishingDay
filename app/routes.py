from flask import render_template, request, redirect, url_for, flash
from app import app

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
	city = request.form['location'].upper()
	try:
		lat, lon, meteo_data = utils.get_meteo_for_city(city)
		tides_data = utils.get_tides_for_city(lat, lon)
	except KeyError:
		flash('Aucun résultat pour la ville cherchée, essayez une autre ville.')
		return redirect(url_for('index'))
	return render_template('result.html', meteo=meteo_data, city=city, \
								tides=tides_data, lat=lat, lon=lon)

@app.route('/about')
def about():
	"""Display information about FishingDay project"""
	return render_template('about.html')

@app.route('/legal')
def legal():
	"""Display legal informations"""
	return render_template('legal.html')

# @app.route('/test_result')
# def test_result():
# 	"""TEST VIEW FOR DEVELOPMENT- TO DELETE"""
# 	lat, lon, meteo_data = utils.get_meteo_for_city('test')
# 	tides_data = utils.get_tides_for_city(lat, lon)
# 	return render_template('test_result.html', city='TEST', meteo=meteo_data, tides=tides_data)