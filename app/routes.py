# from flask import render_template, request, redirect, url_for, flash
# from flask import current_app, Blueprint
# from flask_login import current_user, login_user, logout_user, login_required

# from app import db
# from app import utils
# from app.forms import LocationForm, LoginForm, RegistrationForm
# from app.models import User

# @app.route('/')
# @app.route("/index")*
# def index():
#     """Main page"""
#     form = LocationForm()
#     return render_template('index.html', form=form)


# @app.route('/result', methods=['POST'])
# def result():
#     """View used to display result of the users search"""
#     city = request.form['location']
#     try:
#         lat, lon, meteo_data = utils.get_meteo_for_city(city)
#         tides_data = utils.get_tides_for_city(lat, lon)
#     except KeyError:
#         flash('Aucun résultat pour la ville cherchée, essayez une autre ville.')
#         return redirect(url_for('index'))
#     # if current_user.is_authenticated:
#     #     utils.save_user_search(current_user.id, city, lat, lon)
#     return render_template('result.html', meteo=meteo_data, city=city.upper(), \
#                                 tides=tides_data, lat=lat, lon=lon)

# @app.route('/about')
# def about():
#     """Display information about FishingDay project"""
#     return render_template('about.html')

# @app.route('/legal')
# def legal():
#     """Display legal informations"""
#     return render_template('legal.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """View used for the users to loging in"""
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Utilisateur inconnu ou mot de passe incorrect')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('index'))
#     return render_template('login.html', form=form)

# @app.route('/logout')
# def logout():
#     """View used to logout user"""
#     logout_user()
#     return redirect(url_for('index'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     """View used by users to create account"""
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Merci pour votre inscription. Connectez-vous pour continuer !')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)


# @app.route('/account')
# @login_required
# def account():
#     """View used to display user account informations"""
#     return render_template('account.html')



# # @app.route('/test_result')
# # def test_result():
# #   """TEST VIEW FOR DEVELOPMENT- TO DELETE"""
# #   lat, lon, meteo_data = utils.get_meteo_for_city('test')
# #   tides_data = utils.get_tides_for_city(lat, lon)
# #   return render_template('test_result.html', city='TEST', meteo=meteo_data, tides=tides_data)