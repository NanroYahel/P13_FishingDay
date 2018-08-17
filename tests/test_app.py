"""File containing all the units test for the application"""

from flask_login import login_user
import pytest

from app import db, create_app
from app import utils
from app.models import User, City, UserSearch
from config import ConfigTest


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Function to avoid using http requests"""
    monkeypatch.delattr("requests.sessions.Session.request")

@pytest.fixture(scope='module')
def client():
    """Fixture to create a testing app instance """
    flask_app = create_app(ConfigTest)
    client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield client

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    """Create an instance of flask app with a test db"""
    db.create_all()

    #Insert 1 user, 1 city an 1 search
    user = User(username='Cartman', email='eric@cartman.com')
    user.set_password('password')
    city = City(name='South Park', lat=39.22, lon=-105.99)
    db.session.add(user)
    db.session.add(city)
    search = UserSearch(user_id=1, city_id=1, count=1)
    db.session.add(search)

    db.session.commit()

    yield db

    db.drop_all()

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


########## Testing Flask routes ###########

class TestRoutes(object):
    """Class for testing the status code of the differents views"""

    # #Create a testing instance of the app
    # app = app.test_client()

    def test_index_route(self, client):
        """Test that the index view return a 200 code"""
        rv = client.get('/')
        assert rv.status_code == 200

    def test_about_route(self, client):
        """Test that the about view return a 200 code"""
        rv = client.get('/about')
        assert rv.status_code == 200

    def test_legal_route(self, client):
        """Test that the legal view return a 200 code"""
        rv = client.get('/legal')
        assert rv.status_code == 200

    def test_result_route(self, client, monkeypatch):
        """Test that the result view get 200 code with POST request and 405 with GET"""
        def mockreturn_meteo(city):
            """Return an imitation of meteo result"""
            meteo_day = utils.MeteoDay({'main': {'temp_min': 289.35, 'humidity': 100, \
                                        'pressure': 1035.84, 'temp_max': 290.259, \
                                        'temp': 289.35, 'sea_level': 1036.54, \
                                        'grnd_level': 1035.84, 'temp_kf': -0.91}, \
                                        'dt': 1533114000, 'wind': {'deg': 359.501, \
                                        'speed': 2.86}, 'dt_txt': '2018-08-01 09:00:00', \
                                        'clouds': {'all': 20}, 'weather': [{'icon': '02d', \
                                        'description': 'few clouds', 'id': 801, \
                                        'main': 'Clouds'}], 'sys': {'pod': 'd'}})
            lat = 3.56
            lon = 45.5
            list_meteo_day = [meteo_day, meteo_day]
            return lat, lon, list_meteo_day

        def mockreturn_tides(lat, lon):
            """Return the result of the 1st August for 'Vannes' city"""
            tide_extreme = utils.TideExtreme({'type': 'Low', 'date': '2018-08-07T05:53+0000', \
                                                'dt': 1533621195, 'height': -1.508})
            list_tides_extreme = [tide_extreme, tide_extreme, tide_extreme, tide_extreme, \
                                    tide_extreme, tide_extreme, tide_extreme, tide_extreme, \
                                    tide_extreme, tide_extreme]
            return list_tides_extreme

        monkeypatch.setattr(utils, 'get_meteo_for_city', mockreturn_meteo)
        monkeypatch.setattr(utils, 'get_tides_for_city', mockreturn_tides)
        rv_post = client.post('/result', data={'location':'test'})
        rv_get = client.get('result')
        assert rv_post.status_code == 200
        assert rv_get.status_code == 405

    def test_account_route(self, client, init_database):
        """Test that the account view return the elements in the database for the user Cartman"""
        login(client, 'eric@cartman.com', 'password')
        rv = client.get('/account')
        assert rv.status_code == 200
        assert b"Cartman" in rv.data
        assert b"SOUTH PARK" in rv.data


########## Testing functions of 'utils.py' module #######

class TestUtils(object):
    """Test the functions of 'utils.py' module"""

    def test_convert_direction(self):
        """Convert 200° to SSW"""
        result_test = utils.convert_direction(200)
        assert result_test == 'SSO'

    def test_convert_temp(self):
        """Convert 300°K to 27°C"""
        result_test = utils.convert_temp(300)
        assert result_test == 27

    def test_convert_wind_speed(self):
        """Convert 3 m/s to 6 Kts"""
        result_test = utils.convert_wind_speed(3)
        assert result_test == 6

    def test_get_meteo_for_city(self, client, monkeypatch):
        """Test the result of the function with a mock instead of the api result"""

        def mockreturn(url):
            """Return the result of the 1st August for 'Vannes' city"""
            return {'cod': '200', 'list': [{'main': {'temp_min': 289.35, 'humidity': 100, \
                    'pressure': 1035.84, 'temp_max': 290.259, 'temp': 289.35, \
                    'sea_level': 1036.54, 'grnd_level': 1035.84, 'temp_kf': -0.91}, \
                    'dt': 1533114000, 'wind': {'deg': 359.501, 'speed': 2.86}, \
                    'dt_txt': '2018-08-01 09:00:00', 'clouds': {'all': 20}, \
                    'weather': [{'icon': '02d', 'description': 'few clouds', 'id': 801, \
                    'main': 'Clouds'}], 'sys': {'pod': 'd'}}], 'message': 0.0026, \
                    'city': {'country': 'FR', 'coord': {'lat': 47.6587, 'lon': -2.76}, \
                    'population': 54020, 'name': 'Vannes', 'id': 2970777}, 'cnt': 40}

        monkeypatch.setattr(utils, 'request_api', mockreturn)
        lat_test, lon_test, test_result = utils.get_meteo_for_city('test')

        assert lat_test == 47.6587
        assert lon_test == -2.76
        assert len(test_result) == 1
        assert test_result[0].date.strftime('%H') == '11'
        assert test_result[0].img == '02d'
        assert test_result[0].cloud == 20
        assert test_result[0].temp == 16
        assert test_result[0].wind_direction == 'N'
        assert test_result[0].wind_degree == 359
        assert test_result[0].wind_speed == 6

    def test_get_tides_for_city(self, client, monkeypatch):
        """Test the result of the function with a mock instead of the api result"""

        def mockreturn(url):
            """Return the result of August the 7 for lat=47.619 and lon=-2.737"""
            return {'atlas': 'TPXO_8_v1', 'responseLon': -2.6667, 'extremes': [{'type': 'Low', \
                    'date': '2018-08-07T05:53+0000', 'dt': 1533621195, 'height': -1.508}],\
                     'responseLat': 47.5, 'status': 200, 'requestLat': 47.619, 'callCount': 1, \
                     'requestLon': -2.737}

        monkeypatch.setattr(utils, 'request_api', mockreturn)
        test_result = utils.get_tides_for_city(-2.6667, 47.5)

        assert len(test_result) == 1
        assert test_result[0].time.strftime('%H:%M') == '07:53'
        assert test_result[0].day == 'Mardi'
        assert test_result[0].type == 'BM'
        assert test_result[0].height == -1.51

    def test_find_city(self, client, init_database):
        """Test the function with the city 'South Park' should return : 1
        Then test the function with the city 'Denver' should retrun False"""
        assert utils.find_city('South Park', 39.22, -105.99) == 1
        assert utils.find_city('Denver', 39.44, -104.59) is False

    def test_save_city(self, client, init_database):
        """Check if a city is correctly saved by the function 'save_city'"""
        utils.save_city('Denver', 39.44, -104.59)
        assert City.query.filter_by(name='Denver').first().name == 'Denver'

    def test_save_search(self, client, init_database):
        """Check if a search is correctly saved by the function 'save_search'"""

        #Test that the search doesn't exists already
        assert UserSearch.query.filter_by(user_id=1, city_id=2).first() is None
        #Save a new city in the database and get its 'id'
        utils.save_city('Denver', 39.44, -104.59)
        id_new_city = utils.find_city('Denver', 39.44, -104.59)
        #Save the new_search
        utils.save_search(1, id_new_city)
        assert UserSearch.query.filter_by(user_id=1, city_id=id_new_city).first() is not None

    def test_save_user_search(self, client, init_database):
        #Save a user search that already exists
        utils.save_user_search(1, 'South Park', 39.22, -105.99)
        #Count may return 2
        assert UserSearch.query.filter_by(user_id=1, city_id=1).first().count == 2

        #Save a new user search with a existant city
        #Test that the user search doesn't exists already
        assert UserSearch.query.filter_by(user_id=1, city_id=4).first() is None
        city = City(name='Cheyenne', lat=41.13, lon=-104.80)
        db.session.add(city)
        db.session.commit()
        utils.save_user_search(1, 'Cheyenne', 41.13, -104.80)
        #Then test that the user search exists
        assert UserSearch.query.filter_by(user_id=1, city_id=4).first() is not None

        #Save a new user search with a non existant city
        #Test that the user search doesn't exists already
        assert UserSearch.query.filter_by(user_id=1, city_id=5).first() is None
        utils.save_user_search(1, 'Fort Collins', 40.55, -105.04)
        #Then test that the user search exists
        assert UserSearch.query.filter_by(user_id=1, city_id=5).first() is not None
