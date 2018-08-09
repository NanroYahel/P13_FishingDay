#File containing all the units test for the application

import json
from datetime import datetime

import pytest

from app import app
from app import utils

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Function to avoid using http requests"""
    monkeypatch.delattr("requests.sessions.Session.request")


########## Testing Flask routes ###########

class TestRoutes(object):
    """Class for testing the status code of the differents views"""

    #Create a testing instance of the app
    app = app.test_client()

    def test_index_route(self):
        """Test that the index view return a 200 code"""
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_about_route(self):
        """Test that the about view return a 200 code"""
        rv = self.app.get('/about')
        assert rv.status_code == 200

    def test_legal_route(self):
        """Test that the legal view return a 200 code"""
        rv = self.app.get('/legal')
        assert rv.status_code == 200

    def test_result_route(self, monkeypatch):
        """Test that the result view get 200 code with POST request and 405 with GET"""
        def mockreturn_meteo(city):
            """Return an imitation of meteo result"""
            meteo_day = utils.MeteoDay({'main': {'temp_min': 289.35, 'humidity': 100, 'pressure': 1035.84, 'temp_max': 290.259, 'temp': 289.35, 'sea_level': 1036.54, 'grnd_level': 1035.84, 'temp_kf': -0.91}, 'dt': 1533114000, 'wind': {'deg': 359.501, 'speed': 2.86}, 'dt_txt': '2018-08-01 09:00:00', 'clouds': {'all': 20}, 'weather': [{'icon': '02d', 'description': 'few clouds', 'id': 801, 'main': 'Clouds'}], 'sys': {'pod': 'd'}})
            lat = 3.56
            lon = 45.5
            list_meteo_day = [meteo_day, meteo_day]
            return lat, lon, list_meteo_day

        def mockreturn_tides(lat, lon):
            """Return the result of the 1st August for 'Vannes' city"""
            tide_extreme = utils.TideExtreme({'type': 'Low', 'date': '2018-08-07T05:53+0000', 'dt': 1533621195, 'height': -1.508})
            list_tides_extreme = [tide_extreme, tide_extreme, tide_extreme, tide_extreme, tide_extreme, tide_extreme, tide_extreme, tide_extreme, tide_extreme, tide_extreme]
            return list_tides_extreme

        monkeypatch.setattr(utils, 'get_meteo_for_city', mockreturn_meteo)
        monkeypatch.setattr(utils, 'get_tides_for_city', mockreturn_tides)
        rv_post = self.app.post('/result', data={'location':'test'})
        rv_get = self.app.get('result')
        assert rv_post.status_code == 200
        assert rv_get.status_code == 405


########## Testing functions of 'utils.py' module #######

class TestUtils(object):
    """Test the functions of 'utils.py' module"""

    def test_convert_direction(self):
        """Convert 200° to SSW"""
        result_test = utils.convert_direction(200)
        assert result_test == 'SSW'

    def test_convert_temp(self):
        """Convert 300°K to 27°C"""
        result_test = utils.convert_temp(300)
        assert result_test == 27

    def test_convert_wind_speed(self):
        """Convert 3 m/s to 6 Kts"""
        result_test = utils.convert_wind_speed(3)
        assert result_test == 6

    def test_get_meteo_for_city(self, monkeypatch):
        """Test the result of the function with a mock instead of the api result"""

        def mockreturn(url):
            """Return the result of the 1st August for 'Vannes' city"""
            return {'cod': '200', 'list': [{'main': {'temp_min': 289.35, 'humidity': 100, 'pressure': 1035.84, 'temp_max': 290.259, 'temp': 289.35, 'sea_level': 1036.54, 'grnd_level': 1035.84, 'temp_kf': -0.91}, 'dt': 1533114000, 'wind': {'deg': 359.501, 'speed': 2.86}, 'dt_txt': '2018-08-01 09:00:00', 'clouds': {'all': 20}, 'weather': [{'icon': '02d', 'description': 'few clouds', 'id': 801, 'main': 'Clouds'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 290.83, 'humidity': 97, 'pressure': 1035.32, 'temp_max': 291.516, 'temp': 290.83, 'sea_level': 1036, 'grnd_level': 1035.32, 'temp_kf': -0.68}, 'dt': 1533124800, 'wind': {'deg': 291.008, 'speed': 2.45}, 'dt_txt': '2018-08-01 12:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 291.79, 'humidity': 92, 'pressure': 1034.93, 'temp_max': 292.243, 'temp': 291.79, 'sea_level': 1035.51, 'grnd_level': 1034.93, 'temp_kf': -0.45}, 'dt': 1533135600, 'wind': {'deg': 282.502, 'speed': 4.97}, 'dt_txt': '2018-08-01 15:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 292.4, 'humidity': 90, 'pressure': 1034.32, 'temp_max': 292.626, 'temp': 292.4, 'sea_level': 1034.93, 'grnd_level': 1034.32, 'temp_kf': -0.23}, 'dt': 1533146400, 'wind': {'deg': 288.002, 'speed': 5.92}, 'dt_txt': '2018-08-01 18:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 292.562, 'humidity': 89, 'pressure': 1034.42, 'temp_max': 292.562, 'temp': 292.562, 'sea_level': 1035.27, 'grnd_level': 1034.42, 'temp_kf': 0}, 'dt': 1533157200, 'wind': {'deg': 294.001, 'speed': 5.91}, 'dt_txt': '2018-08-01 21:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 292.192, 'humidity': 91, 'pressure': 1034.75, 'temp_max': 292.192, 'temp': 292.192, 'sea_level': 1035.53, 'grnd_level': 1034.75, 'temp_kf': 0}, 'dt': 1533168000, 'wind': {'deg': 1.50055, 'speed': 5.38}, 'dt_txt': '2018-08-02 00:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 290.914, 'humidity': 98, 'pressure': 1034.63, 'temp_max': 290.914, 'temp': 290.914, 'sea_level': 1035.48, 'grnd_level': 1034.63, 'temp_kf': 0}, 'dt': 1533178800, 'wind': {'deg': 37.5052, 'speed': 7.51}, 'dt_txt': '2018-08-02 03:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 290.815, 'humidity': 99, 'pressure': 1035.24, 'temp_max': 290.815, 'temp': 290.815, 'sea_level': 1036.05, 'grnd_level': 1035.24, 'temp_kf': 0}, 'dt': 1533189600, 'wind': {'deg': 44.0018, 'speed': 7.21}, 'dt_txt': '2018-08-02 06:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 292.985, 'humidity': 87, 'pressure': 1035.83, 'temp_max': 292.985, 'temp': 292.985, 'sea_level': 1036.56, 'grnd_level': 1035.83, 'temp_kf': 0}, 'dt': 1533200400, 'wind': {'deg': 46.5005, 'speed': 5.12}, 'dt_txt': '2018-08-02 09:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 294.9, 'humidity': 80, 'pressure': 1035.16, 'temp_max': 294.9, 'temp': 294.9, 'sea_level': 1035.89, 'grnd_level': 1035.16, 'temp_kf': 0}, 'dt': 1533211200, 'wind': {'deg': 45.5011, 'speed': 2.51}, 'dt_txt': '2018-08-02 12:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 295.07, 'humidity': 79, 'pressure': 1034.32, 'temp_max': 295.07, 'temp': 295.07, 'sea_level': 1034.93, 'grnd_level': 1034.32, 'temp_kf': 0}, 'dt': 1533222000, 'wind': {'deg': 343.504, 'speed': 0.42}, 'dt_txt': '2018-08-02 15:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 295.907, 'humidity': 75, 'pressure': 1033.43, 'temp_max': 295.907, 'temp': 295.907, 'sea_level': 1034.19, 'grnd_level': 1033.43, 'temp_kf': 0}, 'dt': 1533232800, 'wind': {'deg': 298.501, 'speed': 1.85}, 'dt_txt': '2018-08-02 18:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 296.424, 'humidity': 73, 'pressure': 1033.88, 'temp_max': 296.424, 'temp': 296.424, 'sea_level': 1034.73, 'grnd_level': 1033.88, 'temp_kf': 0}, 'dt': 1533243600, 'wind': {'deg': 4.50302, 'speed': 3.72}, 'dt_txt': '2018-08-02 21:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 294.496, 'humidity': 81, 'pressure': 1034.33, 'temp_max': 294.496, 'temp': 294.496, 'sea_level': 1035.11, 'grnd_level': 1034.33, 'temp_kf': 0}, 'dt': 1533254400, 'wind': {'deg': 28.5003, 'speed': 7.55}, 'dt_txt': '2018-08-03 00:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 293.261, 'humidity': 87, 'pressure': 1034.02, 'temp_max': 293.261, 'temp': 293.261, 'sea_level': 1034.8, 'grnd_level': 1034.02, 'temp_kf': 0}, 'dt': 1533265200, 'wind': {'deg': 35.5003, 'speed': 7.33}, 'dt_txt': '2018-08-03 03:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 293.106, 'humidity': 87, 'pressure': 1034.13, 'temp_max': 293.106, 'temp': 293.106, 'sea_level': 1034.93, 'grnd_level': 1034.13, 'temp_kf': 0}, 'dt': 1533276000, 'wind': {'deg': 54.5013, 'speed': 6.91}, 'dt_txt': '2018-08-03 06:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 295.366, 'humidity': 77, 'pressure': 1034.53, 'temp_max': 295.366, 'temp': 295.366, 'sea_level': 1035.42, 'grnd_level': 1034.53, 'temp_kf': 0}, 'dt': 1533286800, 'wind': {'deg': 65.0037, 'speed': 4.76}, 'dt_txt': '2018-08-03 09:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 296.014, 'humidity': 75, 'pressure': 1034.3, 'temp_max': 296.014, 'temp': 296.014, 'sea_level': 1035.05, 'grnd_level': 1034.3, 'temp_kf': 0}, 'dt': 1533297600, 'wind': {'deg': 83.0045, 'speed': 1.71}, 'dt_txt': '2018-08-03 12:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 297.034, 'humidity': 72, 'pressure': 1033.58, 'temp_max': 297.034, 'temp': 297.034, 'sea_level': 1034.2, 'grnd_level': 1033.58, 'temp_kf': 0}, 'dt': 1533308400, 'wind': {'deg': 260.501, 'speed': 2.22}, 'dt_txt': '2018-08-03 15:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 297.644, 'humidity': 70, 'pressure': 1033.01, 'temp_max': 297.644, 'temp': 297.644, 'sea_level': 1033.64, 'grnd_level': 1033.01, 'temp_kf': 0}, 'dt': 1533319200, 'wind': {'deg': 291.501, 'speed': 5.82}, 'dt_txt': '2018-08-03 18:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 297.215, 'humidity': 71, 'pressure': 1033.28, 'temp_max': 297.215, 'temp': 297.215, 'sea_level': 1034.04, 'grnd_level': 1033.28, 'temp_kf': 0}, 'dt': 1533330000, 'wind': {'deg': 299.504, 'speed': 5.5}, 'dt_txt': '2018-08-03 21:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 296.109, 'humidity': 75, 'pressure': 1033.72, 'temp_max': 296.109, 'temp': 296.109, 'sea_level': 1034.58, 'grnd_level': 1033.72, 'temp_kf': 0}, 'dt': 1533340800, 'wind': {'deg': 28.0058, 'speed': 6.61}, 'dt_txt': '2018-08-04 00:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 294.707, 'humidity': 80, 'pressure': 1033.58, 'temp_max': 294.707, 'temp': 294.707, 'sea_level': 1034.38, 'grnd_level': 1033.58, 'temp_kf': 0}, 'dt': 1533351600, 'wind': {'deg': 34.0013, 'speed': 6.17}, 'dt_txt': '2018-08-04 03:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 293.761, 'humidity': 85, 'pressure': 1034, 'temp_max': 293.761, 'temp': 293.761, 'sea_level': 1034.74, 'grnd_level': 1034, 'temp_kf': 0}, 'dt': 1533362400, 'wind': {'deg': 39.0046, 'speed': 6.12}, 'dt_txt': '2018-08-04 06:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 296.088, 'humidity': 75, 'pressure': 1034.46, 'temp_max': 296.088, 'temp': 296.088, 'sea_level': 1035.25, 'grnd_level': 1034.46, 'temp_kf': 0}, 'dt': 1533373200, 'wind': {'deg': 27.0057, 'speed': 4.57}, 'dt_txt': '2018-08-04 09:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 297.368, 'humidity': 71, 'pressure': 1034.36, 'temp_max': 297.368, 'temp': 297.368, 'sea_level': 1035.08, 'grnd_level': 1034.36, 'temp_kf': 0}, 'dt': 1533384000, 'wind': {'deg': 22.0018, 'speed': 2.37}, 'dt_txt': '2018-08-04 12:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 297.41, 'humidity': 72, 'pressure': 1033.58, 'temp_max': 297.41, 'temp': 297.41, 'sea_level': 1034.29, 'grnd_level': 1033.58, 'temp_kf': 0}, 'dt': 1533394800, 'wind': {'deg': 285.501, 'speed': 1.51}, 'dt_txt': '2018-08-04 15:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 298.194, 'humidity': 69, 'pressure': 1032.87, 'temp_max': 298.194, 'temp': 298.194, 'sea_level': 1033.6, 'grnd_level': 1032.87, 'temp_kf': 0}, 'dt': 1533405600, 'wind': {'deg': 280.002, 'speed': 3.78}, 'dt_txt': '2018-08-04 18:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 297.699, 'humidity': 70, 'pressure': 1033.75, 'temp_max': 297.699, 'temp': 297.699, 'sea_level': 1034.54, 'grnd_level': 1033.75, 'temp_kf': 0}, 'dt': 1533416400, 'wind': {'deg': 1.00171, 'speed': 4.82}, 'dt_txt': '2018-08-04 21:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 295.297, 'humidity': 81, 'pressure': 1033.92, 'temp_max': 295.297, 'temp': 295.297, 'sea_level': 1034.74, 'grnd_level': 1033.92, 'temp_kf': 0}, 'dt': 1533427200, 'wind': {'deg': 29.5004, 'speed': 6.92}, 'dt_txt': '2018-08-05 00:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 293.805, 'humidity': 88, 'pressure': 1033.13, 'temp_max': 293.805, 'temp': 293.805, 'sea_level': 1033.96, 'grnd_level': 1033.13, 'temp_kf': 0}, 'dt': 1533438000, 'wind': {'deg': 34.5053, 'speed': 5.86}, 'dt_txt': '2018-08-05 03:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 293.276, 'humidity': 90, 'pressure': 1032.91, 'temp_max': 293.276, 'temp': 293.276, 'sea_level': 1033.72, 'grnd_level': 1032.91, 'temp_kf': 0}, 'dt': 1533448800, 'wind': {'deg': 33.0023, 'speed': 4.9}, 'dt_txt': '2018-08-05 06:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 295.129, 'humidity': 81, 'pressure': 1033.19, 'temp_max': 295.129, 'temp': 295.129, 'sea_level': 1033.92, 'grnd_level': 1033.19, 'temp_kf': 0}, 'dt': 1533459600, 'wind': {'deg': 12.5024, 'speed': 2.67}, 'dt_txt': '2018-08-05 09:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 296.272, 'humidity': 78, 'pressure': 1032.86, 'temp_max': 296.272, 'temp': 296.272, 'sea_level': 1033.54, 'grnd_level': 1032.86, 'temp_kf': 0}, 'dt': 1533470400, 'wind': {'deg': 277, 'speed': 1.92}, 'dt_txt': '2018-08-05 12:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 297.513, 'humidity': 73, 'pressure': 1031.55, 'temp_max': 297.513, 'temp': 297.513, 'sea_level': 1032.25, 'grnd_level': 1031.55, 'temp_kf': 0}, 'dt': 1533481200, 'wind': {'deg': 273, 'speed': 4.87}, 'dt_txt': '2018-08-05 15:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 297.28, 'humidity': 74, 'pressure': 1030.37, 'temp_max': 297.28, 'temp': 297.28, 'sea_level': 1031.05, 'grnd_level': 1030.37, 'temp_kf': 0}, 'dt': 1533492000, 'wind': {'deg': 282.501, 'speed': 6.08}, 'dt_txt': '2018-08-05 18:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}, {'main': {'temp_min': 296.379, 'humidity': 76, 'pressure': 1030.37, 'temp_max': 296.379, 'temp': 296.379, 'sea_level': 1031.18, 'grnd_level': 1030.37, 'temp_kf': 0}, 'dt': 1533502800, 'wind': {'deg': 295.502, 'speed': 6.22}, 'dt_txt': '2018-08-05 21:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 296.452, 'humidity': 76, 'pressure': 1030.08, 'temp_max': 296.452, 'temp': 296.452, 'sea_level': 1030.93, 'grnd_level': 1030.08, 'temp_kf': 0}, 'dt': 1533513600, 'wind': {'deg': 20.0001, 'speed': 6.36}, 'dt_txt': '2018-08-06 00:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 295.383, 'humidity': 81, 'pressure': 1029.06, 'temp_max': 295.383, 'temp': 295.383, 'sea_level': 1029.86, 'grnd_level': 1029.06, 'temp_kf': 0}, 'dt': 1533524400, 'wind': {'deg': 39.5, 'speed': 5.31}, 'dt_txt': '2018-08-06 03:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01n', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'n'}}, {'main': {'temp_min': 295.273, 'humidity': 81, 'pressure': 1028.71, 'temp_max': 295.273, 'temp': 295.273, 'sea_level': 1029.53, 'grnd_level': 1028.71, 'temp_kf': 0}, 'dt': 1533535200, 'wind': {'deg': 82.0003, 'speed': 6.26}, 'dt_txt': '2018-08-06 06:00:00', 'clouds': {'all': 0}, 'weather': [{'icon': '01d', 'description': 'clear sky', 'id': 800, 'main': 'Clear'}], 'sys': {'pod': 'd'}}], 'message': 0.0026, 'city': {'country': 'FR', 'coord': {'lat': 47.6587, 'lon': -2.76}, 'population': 54020, 'name': 'Vannes', 'id': 2970777}, 'cnt': 40}

        monkeypatch.setattr(utils, 'request_api', mockreturn)
        lat_test, lon_test, test_result = utils.get_meteo_for_city('test')

        assert lat_test == 47.6587
        assert lon_test == -2.76
        assert len(test_result) == 40
        assert test_result[0].date.strftime('%H') == '11'
        assert test_result[0].img == '02d'
        assert test_result[0].cloud == 20
        assert test_result[0].temp == 16
        assert test_result[0].wind_direction == 'N'
        assert test_result[0].wind_degree == 359 
        assert test_result[0].wind_speed == 6

    def test_get_tides_for_city(self, monkeypatch):
        """Test the result of the function with a mock instead of the api result"""

        def mockreturn(url):
            """Return the result of August the 7 for lat=47.619 and lon=-2.737"""
            return {'atlas': 'TPXO_8_v1', 'responseLon': -2.6667, 'extremes': [{'type': 'Low', 'date': '2018-08-07T05:53+0000', 'dt': 1533621195, 'height': -1.508}, {'type': 'High', 'date': '2018-08-07T12:22+0000', 'dt': 1533644556, 'height': 1.244}, {'type': 'Low', 'date': '2018-08-07T18:28+0000', 'dt': 1533666490, 'height': -1.606}, {'type': 'High', 'date': '2018-08-08T01:00+0000', 'dt': 1533690026, 'height': 1.336}, {'type': 'Low', 'date': '2018-08-08T06:59+0000', 'dt': 1533711544, 'height': -1.711}, {'type': 'High', 'date': '2018-08-08T13:30+0000', 'dt': 1533735026, 'height': 1.545}, {'type': 'Low', 'date': '2018-08-08T19:31+0000', 'dt': 1533756718, 'height': -1.903}, {'type': 'High', 'date': '2018-08-09T02:00+0000', 'dt': 1533780049, 'height': 1.604}, {'type': 'Low', 'date': '2018-08-09T07:57+0000', 'dt': 1533801478, 'height': -1.994}, {'type': 'High', 'date': '2018-08-09T14:22+0000', 'dt': 1533824571, 'height': 1.866}, {'type': 'Low', 'date': '2018-08-09T20:28+0000', 'dt': 1533846486, 'height': -2.239}], 'responseLat': 47.5, 'status': 200, 'requestLat': 47.619, 'callCount': 1, 'copyright': 'Tidal data retrieved from www.worldtide.info. Copyright (c) 2014-2017 Brainware LLC. Licensed for use of individual spatial coordinates on behalf of/by an end-user. Copyright (c) 2010-2016 Oregon State University. Licensed for individual spatial coordinates via ModEM-Geophysics Inc. NO GUARANTEES ARE MADE ABOUT THE CORRECTNESS OF THIS DATA. You may not use it if anyone or anything could come to harm as a result of using it (e.g. for navigational purposes).', 'requestLon': -2.737}

        monkeypatch.setattr(utils, 'request_api', mockreturn)
        test_result = utils.get_tides_for_city(-2.6667, 47.5)

        assert len(test_result) == 11
        assert test_result[0].time.strftime('%H:%M') == '07:53'
        assert test_result[0].day == 'Mardi'
        assert test_result[0].type == 'BM'
        assert test_result[0].height == -1.51

