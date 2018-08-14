"""File containing the function called by the views"""

from datetime import datetime
import calendar
import time
import arrow
import requests as req
from flask import current_app
from app import db
from app.models import User, City, UserSearch


#TO DELETE
mock_meteo = {'city': {'population': 54020, 'country': 'FR', 'coord': {'lat': 47.6587, 'lon': -2.76}, 'id': 2970777, 'name': 'Vannes'}, 'cnt': 40, 'message': 0.013, 'list': [{'rain': {'3h': 1.6975}, 'clouds': {'all': 56}, 'main': {'grnd_level': 1027.89, 'temp': 293.27, 'temp_kf': 3.05, 'humidity': 100, 'temp_min': 290.223, 'sea_level': 1028.71, 'temp_max': 293.27, 'pressure': 1027.89}, 'wind': {'speed': 2.33, 'deg': 329.501}, 'dt': 1533729600, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-08 12:00:00'}, {'rain': {'3h': 0.0225}, 'clouds': {'all': 88}, 'main': {'grnd_level': 1027.31, 'temp': 293.39, 'temp_kf': 2.29, 'humidity': 100, 'temp_min': 291.101, 'sea_level': 1028.01, 'temp_max': 293.39, 'pressure': 1027.31}, 'wind': {'speed': 3.67, 'deg': 297.504}, 'dt': 1533740400, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-08 15:00:00'}, {'rain': {}, 'clouds': {'all': 88}, 'main': {'grnd_level': 1026.9, 'temp': 292.9, 'temp_kf': 1.52, 'humidity': 99, 'temp_min': 291.376, 'sea_level': 1027.56, 'temp_max': 292.9, 'pressure': 1026.9}, 'wind': {'speed': 6.11, 'deg': 290.004}, 'dt': 1533751200, 'sys': {'pod': 'd'}, 'weather': [{'icon': '04d', 'main': 'Clouds', 'id': 804, 'description': 'overcast clouds'}], 'dt_txt': '2018-08-08 18:00:00'}, {'rain': {}, 'clouds': {'all': 92}, 'main': {'grnd_level': 1027.2, 'temp': 291.98, 'temp_kf': 0.76, 'humidity': 99, 'temp_min': 291.219, 'sea_level': 1028.02, 'temp_max': 291.98, 'pressure': 1027.2}, 'wind': {'speed': 8.11, 'deg': 314.501}, 'dt': 1533762000, 'sys': {'pod': 'n'}, 'weather': [{'icon': '04n', 'main': 'Clouds', 'id': 804, 'description': 'overcast clouds'}], 'dt_txt': '2018-08-08 21:00:00'}, {'rain': {'3h': 0.595}, 'clouds': {'all': 92}, 'main': {'grnd_level': 1027.69, 'temp': 289.604, 'temp_kf': 0, 'humidity': 100, 'temp_min': 289.604, 'sea_level': 1028.35, 'temp_max': 289.604, 'pressure': 1027.69}, 'wind': {'speed': 6.36, 'deg': 342.503}, 'dt': 1533772800, 'sys': {'pod': 'n'}, 'weather': [{'icon': '10n', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-09 00:00:00'}, {'rain': {'3h': 4.765}, 'clouds': {'all': 92}, 'main': {'grnd_level': 1026.99, 'temp': 287.875, 'temp_kf': 0, 'humidity': 100, 'temp_min': 287.875, 'sea_level': 1027.65, 'temp_max': 287.875, 'pressure': 1026.99}, 'wind': {'speed': 5.11, 'deg': 329.001}, 'dt': 1533783600, 'sys': {'pod': 'n'}, 'weather': [{'icon': '10n', 'main': 'Rain', 'id': 501, 'description': 'moderate rain'}], 'dt_txt': '2018-08-09 03:00:00'}, {'rain': {'3h': 0.745}, 'clouds': {'all': 56}, 'main': {'grnd_level': 1027.14, 'temp': 288.243, 'temp_kf': 0, 'humidity': 100, 'temp_min': 288.243, 'sea_level': 1027.86, 'temp_max': 288.243, 'pressure': 1027.14}, 'wind': {'speed': 2.72, 'deg': 309.002}, 'dt': 1533794400, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-09 06:00:00'}, {'rain': {'3h': 0.015000000000001}, 'clouds': {'all': 32}, 'main': {'grnd_level': 1029.03, 'temp': 289.426, 'temp_kf': 0, 'humidity': 100, 'temp_min': 289.426, 'sea_level': 1029.92, 'temp_max': 289.426, 'pressure': 1029.03}, 'wind': {'speed': 6.46, 'deg': 305.509}, 'dt': 1533805200, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-09 09:00:00'}, {'rain': {}, 'clouds': {'all': 12}, 'main': {'grnd_level': 1031.29, 'temp': 290.905, 'temp_kf': 0, 'humidity': 100, 'temp_min': 290.905, 'sea_level': 1032.06, 'temp_max': 290.905, 'pressure': 1031.29}, 'wind': {'speed': 6.47, 'deg': 299.003}, 'dt': 1533816000, 'sys': {'pod': 'd'}, 'weather': [{'icon': '02d', 'main': 'Clouds', 'id': 801, 'description': 'few clouds'}], 'dt_txt': '2018-08-09 12:00:00'}, {'rain': {}, 'clouds': {'all': 0}, 'main': {'grnd_level': 1032.56, 'temp': 291.202, 'temp_kf': 0, 'humidity': 99, 'temp_min': 291.202, 'sea_level': 1033.34, 'temp_max': 291.202, 'pressure': 1032.56}, 'wind': {'speed': 8.57, 'deg': 283.5}, 'dt': 1533826800, 'sys': {'pod': 'd'}, 'weather': [{'icon': '01d', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-09 15:00:00'}, {'rain': {}, 'clouds': {'all': 0}, 'main': {'grnd_level': 1033.85, 'temp': 290.914, 'temp_kf': 0, 'humidity': 100, 'temp_min': 290.914, 'sea_level': 1034.62, 'temp_max': 290.914, 'pressure': 1033.85}, 'wind': {'speed': 8.12, 'deg': 282.503}, 'dt': 1533837600, 'sys': {'pod': 'd'}, 'weather': [{'icon': '01d', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-09 18:00:00'}, {'rain': {}, 'clouds': {'all': 8}, 'main': {'grnd_level': 1035.73, 'temp': 290.386, 'temp_kf': 0, 'humidity': 100, 'temp_min': 290.386, 'sea_level': 1036.47, 'temp_max': 290.386, 'pressure': 1035.73}, 'wind': {'speed': 6.5, 'deg': 285.002}, 'dt': 1533848400, 'sys': {'pod': 'n'}, 'weather': [{'icon': '02n', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-09 21:00:00'}, {'rain': {}, 'clouds': {'all': 32}, 'main': {'grnd_level': 1036.62, 'temp': 290.319, 'temp_kf': 0, 'humidity': 100, 'temp_min': 290.319, 'sea_level': 1037.42, 'temp_max': 290.319, 'pressure': 1036.62}, 'wind': {'speed': 5.17, 'deg': 276.006}, 'dt': 1533859200, 'sys': {'pod': 'n'}, 'weather': [{'icon': '03n', 'main': 'Clouds', 'id': 802, 'description': 'scattered clouds'}], 'dt_txt': '2018-08-10 00:00:00'}, {'rain': {}, 'clouds': {'all': 48}, 'main': {'grnd_level': 1036.89, 'temp': 290.435, 'temp_kf': 0, 'humidity': 100, 'temp_min': 290.435, 'sea_level': 1037.69, 'temp_max': 290.435, 'pressure': 1036.89}, 'wind': {'speed': 4.71, 'deg': 260.004}, 'dt': 1533870000, 'sys': {'pod': 'n'}, 'weather': [{'icon': '03n', 'main': 'Clouds', 'id': 802, 'description': 'scattered clouds'}], 'dt_txt': '2018-08-10 03:00:00'}, {'rain': {}, 'clouds': {'all': 64}, 'main': {'grnd_level': 1037.6, 'temp': 290.618, 'temp_kf': 0, 'humidity': 99, 'temp_min': 290.618, 'sea_level': 1038.37, 'temp_max': 290.618, 'pressure': 1037.6}, 'wind': {'speed': 4.86, 'deg': 255.505}, 'dt': 1533880800, 'sys': {'pod': 'd'}, 'weather': [{'icon': '04d', 'main': 'Clouds', 'id': 803, 'description': 'broken clouds'}], 'dt_txt': '2018-08-10 06:00:00'}, {'rain': {}, 'clouds': {'all': 24}, 'main': {'grnd_level': 1038.62, 'temp': 290.722, 'temp_kf': 0, 'humidity': 99, 'temp_min': 290.722, 'sea_level': 1039.29, 'temp_max': 290.722, 'pressure': 1038.62}, 'wind': {'speed': 4.81, 'deg': 245.501}, 'dt': 1533891600, 'sys': {'pod': 'd'}, 'weather': [{'icon': '02d', 'main': 'Clouds', 'id': 801, 'description': 'few clouds'}], 'dt_txt': '2018-08-10 09:00:00'}, {'rain': {'3h': 0.13}, 'clouds': {'all': 56}, 'main': {'grnd_level': 1039.11, 'temp': 290.955, 'temp_kf': 0, 'humidity': 98, 'temp_min': 290.955, 'sea_level': 1039.67, 'temp_max': 290.955, 'pressure': 1039.11}, 'wind': {'speed': 5.1, 'deg': 238.003}, 'dt': 1533902400, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-10 12:00:00'}, {'rain': {'3h': 0.030000000000001}, 'clouds': {'all': 24}, 'main': {'grnd_level': 1038.66, 'temp': 291.644, 'temp_kf': 0, 'humidity': 95, 'temp_min': 291.644, 'sea_level': 1039.35, 'temp_max': 291.644, 'pressure': 1038.66}, 'wind': {'speed': 4.76, 'deg': 247.002}, 'dt': 1533913200, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-10 15:00:00'}, {'rain': {'3h': 0.004999999999999}, 'clouds': {'all': 24}, 'main': {'grnd_level': 1038.2, 'temp': 291.624, 'temp_kf': 0, 'humidity': 95, 'temp_min': 291.624, 'sea_level': 1038.85, 'temp_max': 291.624, 'pressure': 1038.2}, 'wind': {'speed': 4.2, 'deg': 248.005}, 'dt': 1533924000, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-10 18:00:00'}, {'rain': {}, 'clouds': {'all': 32}, 'main': {'grnd_level': 1038.54, 'temp': 291.184, 'temp_kf': 0, 'humidity': 97, 'temp_min': 291.184, 'sea_level': 1039.27, 'temp_max': 291.184, 'pressure': 1038.54}, 'wind': {'speed': 2.72, 'deg': 245.502}, 'dt': 1533934800, 'sys': {'pod': 'n'}, 'weather': [{'icon': '03n', 'main': 'Clouds', 'id': 802, 'description': 'scattered clouds'}], 'dt_txt': '2018-08-10 21:00:00'}, {'rain': {}, 'clouds': {'all': 12}, 'main': {'grnd_level': 1037.98, 'temp': 290.876, 'temp_kf': 0, 'humidity': 98, 'temp_min': 290.876, 'sea_level': 1038.78, 'temp_max': 290.876, 'pressure': 1037.98}, 'wind': {'speed': 2.72, 'deg': 219.006}, 'dt': 1533945600, 'sys': {'pod': 'n'}, 'weather': [{'icon': '02n', 'main': 'Clouds', 'id': 801, 'description': 'few clouds'}], 'dt_txt': '2018-08-11 00:00:00'}, {'rain': {}, 'clouds': {'all': 56}, 'main': {'grnd_level': 1036.92, 'temp': 290.866, 'temp_kf': 0, 'humidity': 98, 'temp_min': 290.866, 'sea_level': 1037.72, 'temp_max': 290.866, 'pressure': 1036.92}, 'wind': {'speed': 3.03, 'deg': 213.506}, 'dt': 1533956400, 'sys': {'pod': 'n'}, 'weather': [{'icon': '04n', 'main': 'Clouds', 'id': 803, 'description': 'broken clouds'}], 'dt_txt': '2018-08-11 03:00:00'}, {'rain': {}, 'clouds': {'all': 32}, 'main': {'grnd_level': 1036.21, 'temp': 291.034, 'temp_kf': 0, 'humidity': 97, 'temp_min': 291.034, 'sea_level': 1036.95, 'temp_max': 291.034, 'pressure': 1036.21}, 'wind': {'speed': 3.27, 'deg': 193.5}, 'dt': 1533967200, 'sys': {'pod': 'd'}, 'weather': [{'icon': '03d', 'main': 'Clouds', 'id': 802, 'description': 'scattered clouds'}], 'dt_txt': '2018-08-11 06:00:00'}, {'rain': {}, 'clouds': {'all': 8}, 'main': {'grnd_level': 1035.85, 'temp': 291.928, 'temp_kf': 0, 'humidity': 93, 'temp_min': 291.928, 'sea_level': 1036.41, 'temp_max': 291.928, 'pressure': 1035.85}, 'wind': {'speed': 4.06, 'deg': 188.5}, 'dt': 1533978000, 'sys': {'pod': 'd'}, 'weather': [{'icon': '02d', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-11 09:00:00'}, {'rain': {}, 'clouds': {'all': 12}, 'main': {'grnd_level': 1035.17, 'temp': 292.314, 'temp_kf': 0, 'humidity': 92, 'temp_min': 292.314, 'sea_level': 1035.69, 'temp_max': 292.314, 'pressure': 1035.17}, 'wind': {'speed': 4.52, 'deg': 198.002}, 'dt': 1533988800, 'sys': {'pod': 'd'}, 'weather': [{'icon': '02d', 'main': 'Clouds', 'id': 801, 'description': 'few clouds'}], 'dt_txt': '2018-08-11 12:00:00'}, {'rain': {}, 'clouds': {'all': 8}, 'main': {'grnd_level': 1034.04, 'temp': 292.601, 'temp_kf': 0, 'humidity': 91, 'temp_min': 292.601, 'sea_level': 1034.61, 'temp_max': 292.601, 'pressure': 1034.04}, 'wind': {'speed': 3.85, 'deg': 217.5}, 'dt': 1533999600, 'sys': {'pod': 'd'}, 'weather': [{'icon': '02d', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-11 15:00:00'}, {'rain': {}, 'clouds': {'all': 12}, 'main': {'grnd_level': 1032.39, 'temp': 292.632, 'temp_kf': 0, 'humidity': 91, 'temp_min': 292.632, 'sea_level': 1033.05, 'temp_max': 292.632, 'pressure': 1032.39}, 'wind': {'speed': 2.42, 'deg': 237}, 'dt': 1534010400, 'sys': {'pod': 'd'}, 'weather': [{'icon': '02d', 'main': 'Clouds', 'id': 801, 'description': 'few clouds'}], 'dt_txt': '2018-08-11 18:00:00'}, {'rain': {}, 'clouds': {'all': 0}, 'main': {'grnd_level': 1031.54, 'temp': 291.86, 'temp_kf': 0, 'humidity': 96, 'temp_min': 291.86, 'sea_level': 1032.23, 'temp_max': 291.86, 'pressure': 1031.54}, 'wind': {'speed': 1.27, 'deg': 203.504}, 'dt': 1534021200, 'sys': {'pod': 'n'}, 'weather': [{'icon': '01n', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-11 21:00:00'}, {'rain': {}, 'clouds': {'all': 0}, 'main': {'grnd_level': 1030.23, 'temp': 291.427, 'temp_kf': 0, 'humidity': 97, 'temp_min': 291.427, 'sea_level': 1030.95, 'temp_max': 291.427, 'pressure': 1030.23}, 'wind': {'speed': 1.97, 'deg': 198.001}, 'dt': 1534032000, 'sys': {'pod': 'n'}, 'weather': [{'icon': '01n', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-12 00:00:00'}, {'rain': {}, 'clouds': {'all': 32}, 'main': {'grnd_level': 1028.44, 'temp': 291.195, 'temp_kf': 0, 'humidity': 98, 'temp_min': 291.195, 'sea_level': 1029.16, 'temp_max': 291.195, 'pressure': 1028.44}, 'wind': {'speed': 2.04, 'deg': 189.505}, 'dt': 1534042800, 'sys': {'pod': 'n'}, 'weather': [{'icon': '03n', 'main': 'Clouds', 'id': 802, 'description': 'scattered clouds'}], 'dt_txt': '2018-08-12 03:00:00'}, {'rain': {}, 'clouds': {'all': 24}, 'main': {'grnd_level': 1027.68, 'temp': 291.327, 'temp_kf': 0, 'humidity': 98, 'temp_min': 291.327, 'sea_level': 1028.32, 'temp_max': 291.327, 'pressure': 1027.68}, 'wind': {'speed': 3.06, 'deg': 165.505}, 'dt': 1534053600, 'sys': {'pod': 'd'}, 'weather': [{'icon': '02d', 'main': 'Clouds', 'id': 801, 'description': 'few clouds'}], 'dt_txt': '2018-08-12 06:00:00'}, {'rain': {}, 'clouds': {'all': 0}, 'main': {'grnd_level': 1027.44, 'temp': 292.315, 'temp_kf': 0, 'humidity': 93, 'temp_min': 292.315, 'sea_level': 1028.01, 'temp_max': 292.315, 'pressure': 1027.44}, 'wind': {'speed': 2.46, 'deg': 166.003}, 'dt': 1534064400, 'sys': {'pod': 'd'}, 'weather': [{'icon': '01d', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-12 09:00:00'}, {'rain': {'3h': 0.0025000000000013}, 'clouds': {'all': 0}, 'main': {'grnd_level': 1026.73, 'temp': 292.926, 'temp_kf': 0, 'humidity': 90, 'temp_min': 292.926, 'sea_level': 1027.34, 'temp_max': 292.926, 'pressure': 1026.73}, 'wind': {'speed': 2.26, 'deg': 201}, 'dt': 1534075200, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-12 12:00:00'}, {'rain': {}, 'clouds': {'all': 8}, 'main': {'grnd_level': 1025.66, 'temp': 293.311, 'temp_kf': 0, 'humidity': 90, 'temp_min': 293.311, 'sea_level': 1026.26, 'temp_max': 293.311, 'pressure': 1025.66}, 'wind': {'speed': 3.16, 'deg': 239.007}, 'dt': 1534086000, 'sys': {'pod': 'd'}, 'weather': [{'icon': '02d', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-12 15:00:00'}, {'rain': {}, 'clouds': {'all': 0}, 'main': {'grnd_level': 1024.53, 'temp': 293.189, 'temp_kf': 0, 'humidity': 92, 'temp_min': 293.189, 'sea_level': 1025.17, 'temp_max': 293.189, 'pressure': 1024.53}, 'wind': {'speed': 3.91, 'deg': 257.503}, 'dt': 1534096800, 'sys': {'pod': 'd'}, 'weather': [{'icon': '01d', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-12 18:00:00'}, {'rain': {}, 'clouds': {'all': 8}, 'main': {'grnd_level': 1024.33, 'temp': 292.417, 'temp_kf': 0, 'humidity': 95, 'temp_min': 292.417, 'sea_level': 1025.11, 'temp_max': 292.417, 'pressure': 1024.33}, 'wind': {'speed': 3.02, 'deg': 266.004}, 'dt': 1534107600, 'sys': {'pod': 'n'}, 'weather': [{'icon': '02n', 'main': 'Clear', 'id': 800, 'description': 'clear sky'}], 'dt_txt': '2018-08-12 21:00:00'}, {'rain': {'3h': 0.012499999999999}, 'clouds': {'all': 76}, 'main': {'grnd_level': 1024.02, 'temp': 292.115, 'temp_kf': 0, 'humidity': 96, 'temp_min': 292.115, 'sea_level': 1024.78, 'temp_max': 292.115, 'pressure': 1024.02}, 'wind': {'speed': 2.57, 'deg': 242.007}, 'dt': 1534118400, 'sys': {'pod': 'n'}, 'weather': [{'icon': '10n', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-13 00:00:00'}, {'rain': {'3h': 0.012499999999999}, 'clouds': {'all': 92}, 'main': {'grnd_level': 1023.06, 'temp': 292.187, 'temp_kf': 0, 'humidity': 97, 'temp_min': 292.187, 'sea_level': 1023.86, 'temp_max': 292.187, 'pressure': 1023.06}, 'wind': {'speed': 1.96, 'deg': 221.006}, 'dt': 1534129200, 'sys': {'pod': 'n'}, 'weather': [{'icon': '10n', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-13 03:00:00'}, {'rain': {'3h': 0.1875}, 'clouds': {'all': 88}, 'main': {'grnd_level': 1023.22, 'temp': 292.198, 'temp_kf': 0, 'humidity': 97, 'temp_min': 292.198, 'sea_level': 1023.93, 'temp_max': 292.198, 'pressure': 1023.22}, 'wind': {'speed': 2.27, 'deg': 223.501}, 'dt': 1534140000, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-13 06:00:00'}, {'rain': {'3h': 0.0625}, 'clouds': {'all': 88}, 'main': {'grnd_level': 1023.79, 'temp': 292.412, 'temp_kf': 0, 'humidity': 95, 'temp_min': 292.412, 'sea_level': 1024.45, 'temp_max': 292.412, 'pressure': 1023.79}, 'wind': {'speed': 2.26, 'deg': 280.513}, 'dt': 1534150800, 'sys': {'pod': 'd'}, 'weather': [{'icon': '10d', 'main': 'Rain', 'id': 500, 'description': 'light rain'}], 'dt_txt': '2018-08-13 09:00:00'}], 'cod': '200'}
mock_tides = {'atlas': 'TPXO_8_v1', 'responseLon': -2.6667, 'extremes': [{'type': 'Low', 'date': '2018-08-07T05:53+0000', 'dt': 1533621195, 'height': -1.508}, {'type': 'High', 'date': '2018-08-07T12:22+0000', 'dt': 1533644556, 'height': 1.244}, {'type': 'Low', 'date': '2018-08-07T18:28+0000', 'dt': 1533666490, 'height': -1.606}, {'type': 'High', 'date': '2018-08-08T01:00+0000', 'dt': 1533690026, 'height': 1.336}, {'type': 'Low', 'date': '2018-08-08T06:59+0000', 'dt': 1533711544, 'height': -1.711}, {'type': 'High', 'date': '2018-08-08T13:30+0000', 'dt': 1533735026, 'height': 1.545}, {'type': 'Low', 'date': '2018-08-08T19:31+0000', 'dt': 1533756718, 'height': -1.903}, {'type': 'High', 'date': '2018-08-09T02:00+0000', 'dt': 1533780049, 'height': 1.604}, {'type': 'Low', 'date': '2018-08-09T07:57+0000', 'dt': 1533801478, 'height': -1.994}, {'type': 'High', 'date': '2018-08-09T14:22+0000', 'dt': 1533824571, 'height': 1.866}, {'type': 'Low', 'date': '2018-08-09T20:28+0000', 'dt': 1533846486, 'height': -2.239}], 'responseLat': 47.5, 'status': 200, 'requestLat': 47.619, 'callCount': 1, 'copyright': 'Tidal data retrieved from www.worldtide.info. Copyright (c) 2014-2017 Brainware LLC. Licensed for use of individual spatial coordinates on behalf of/by an end-user. Copyright (c) 2010-2016 Oregon State University. Licensed for individual spatial coordinates via ModEM-Geophysics Inc. NO GUARANTEES ARE MADE ABOUT THE CORRECTNESS OF THIS DATA. You may not use it if anyone or anything could come to harm as a result of using it (e.g. for navigational purposes).', 'requestLon': -2.737}

#Constant used to convert wind direction
DIRECTION = {1:'N', 2:'NNE', 3:'NE', 4:'ENE', 5:'E', 6:'ESE', 7:'SE', 8:'SSE', 9:'S', 10:'SSW', \
            11:'SW', 12:'WSW', 13:'W', 14:'WNW', 15:'NW', 16:'NNW', 17:'N'}

####### Function used to get data from differents API

def request_api(url):
    """Request the selected url and return data from the api as json"""
    data = req.get(url)
    return data.json()

def get_meteo_for_city(city):
    """Method to get the meteo data with the api"""
    url = "http://api.openweathermap.org/data/2.5/forecast?q={},fr&mode=json&APPID={}".format(city,\
        current_app.config['OWM_API_KEY'])
    meteo_data = request_api(url)
    # meteo_data = mock_meteo #Use for development
    list_meteo_day = []
    for element in meteo_data['list']:
        new_meteo_day = MeteoDay(element)
        list_meteo_day.append(new_meteo_day)
    lat = meteo_data['city']['coord']['lat']
    lon = meteo_data['city']['coord']['lon']
    return lat, lon, list_meteo_day


def get_tides_for_city(lat, lon):
    """Method to get the tides data with the api"""
    today = time.time()
    url = "https://www.worldtides.info/api?extremes&start={}&length=259200&lat={}&lon={}&key={}".\
            format(today, lat, lon, current_app.config['WT_API_KEY'])
    tides_data = request_api(url)
    # tides_data = mock_tides #Use for development
    list_tides_extreme = []
    for element in tides_data['extremes']:
        new_tide_extreme = TideExtreme(element)
        list_tides_extreme.append(new_tide_extreme)
    return list_tides_extreme


####### Function used to format MeteoDay attributes #######

def convert_direction(direction):
    """Convert degree direction in cardinal direction"""
    number_direction = round(direction/22.5, 0) + 1
    return DIRECTION[number_direction]

def convert_temp(temp_kelvin):
    """Convert kelvin degrees to celsius degrees"""
    temp_celsius = round(temp_kelvin - 273.15)
    return temp_celsius

def convert_wind_speed(speed_ms):
    """Convert wind speed form m/s to Knots"""
    speed_kts = round(speed_ms/0.514, 0)
    return speed_kts

####### Function used to format TideExtreme attributes #######

def convert_type_fr(type_tide):
    """Convert the type of tide in french notation"""
    if type_tide == "High":
        type_tide = "PM"
    elif type_tide == "Low":
        type_tide = "BM"
    return type_tide

def find_weekday(datetime):
    """Find the day of the week from a datetime"""
    weekdays = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    weekday = calendar.weekday(datetime.year, datetime.month, datetime.day)
    return weekdays[weekday]


###### Functions used to interact with the db ######

def save_user_search(user, city, lat, lon):
    """Save the city if it not exists and then save the search"""
    #Check if the city is already in the database
    city_searched = find_city(city, lat, lon)
    if city_searched is not False:
        #Check if the search has already been made by this user if city exists
        check_search = UserSearch.query.get((user, city_searched))
        if check_search is not None:
            #If the search has already been made, increment the count
            check_search.count += 1
            check_search.timestamp = datetime.utcnow()

            db.session.commit()
        else:
            #Save the search
            save_search(user, city_searched)
    else:
        #Save the city if it doesn't exists and then save the search
        save_city(city, lat, lon)
        city_searched = City.query.filter_by(name=city, lat=lat, lon=lon).first()
        save_search(user, city_searched.id)

def find_city(city, lat, lon):
    """Return False if the city doesn't exists in the database or the id if it does """
    city_to_find = City.query.filter_by(name=city, lat=lat, lon=lon)
    if city_to_find.all() == []:
        city_searched = False
    else:
        city_searched = city_to_find.first().id
    return city_searched

def save_city(city, lat, lon):
    """Save a city in the database"""
    city_to_save = City(name=city, lat=lat, lon=lon)
    db.session.add(city_to_save)
    db.session.commit()

def save_search(user_id, city_id):
    """Save a user search in the database"""
    search_to_save = UserSearch(user_id=user_id, city_id=city_id, count=1)
    db.session.add(search_to_save)
    db.session.commit()


####### Classes #######

class MeteoDay:
    """Class containing all the meteo informations for a period"""

    def __init__(self, meteo):
        self.date = arrow.get(meteo['dt']).to('Europe/Paris')
        self.img = meteo['weather'][0]['icon']
        self.cloud = meteo['clouds']['all']
        self.temp = convert_temp(meteo['main']['temp'])
        self.wind_direction = convert_direction(float(meteo['wind']['deg']))
        self.wind_degree = int(meteo['wind']['deg'])
        self.wind_speed = int(convert_wind_speed(meteo['wind']['speed']))

        #Manages the case where there is no rainy day in the period
        try:
            self.rain = round(meteo['rain']['3h'], 2)
        except KeyError:
            self.rain = 0


class TideExtreme:
    """Class containing all the tide informations for a 'tide extreme' """

    def __init__(self, tides):
        self.time = arrow.get(tides['dt']).to('Europe/Paris')
        self.day = find_weekday(self.time)
        self.type = convert_type_fr(tides['type'])
        self.height = round(tides['height'], 2)