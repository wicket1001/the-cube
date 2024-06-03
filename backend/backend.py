import json
from enum import IntFlag, auto
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import serial

import utils
from DebugLevel import DebugLevel
from Physics import SIEncoder, Temperature, Length, Energy
from algorithm_utils import Algorithms

hostName = "localhost"
serverPort = 8080

try:
    arduino = serial.Serial(
        port='/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_44238313938351E04290-if00',
        baudrate=9600,
        timeout=1)
    arduino_found = True
except serial.serialutil.SerialException as e:
    print("ARDUINO NOT FOUND")
    arduino_found = False

absolute_step = 0
benchmark_house = utils.get_house()
decision_house = utils.get_house()
weather = utils.read_csv(DebugLevel.INFORMATIONAL)
cache = []
cache_size = 144


# colors = ['BLACK', 'WHITE', 'RED', 'LIME', 'YELLOW', 'CYAN', 'MAGENTA', 'MAROON', 'OLIVE', 'GREEN']
class Colors(IntFlag):
    BLACK = auto()
    WHITE = auto()
    RED = auto()
    LIME = auto()
    YELLOW = auto()
    CYAN = auto()
    MAGENTA = auto()
    MAROON = auto()
    OLIVE = auto()
    GREEN = auto()

class Strips(IntFlag):
    GRID = auto()
    BATTERY = auto()
    SOLAR_PANEL = auto()
    WIND_TURBINE = auto()
    SOLAR_THERMAL_WATER = auto()
    ATTIC_RIGHT = auto()
    ATTIC_LEFT = auto()
    ATTIC_UP = auto()
    THIRD_RIGHT = auto()
    THIRD_LEFT = auto()
    THIRD_UP = auto()
    SECOND_RIGHT = auto()
    SECOND_LEFT = auto()
    SECOND_UP = auto()
    FIRST_RIGHT = auto()
    FIRST_LEFT = auto()
    HEATPUMP = auto()
    THERMAL_BATTERY = auto()
    WATER_BUFFER_THERMAL_BATTERY = auto()
    WATER_BUFFER_HEATPUMP = auto()
    FIRST_UP_RADIATORS = auto()
    FIRST_RADIATORS = auto()
    SECOND_UP_RADIATORS = auto()
    SECOND_RADIATORS = auto()
    THIRD_UP_RADIATORS = auto()
    THIRD_RADIATORS = auto()

#maxlen = max([len(x) for x in colors])
maxi_value = {}
mini_value = {}


def trim(value: float):
    if value > 1:
        return 1
    elif value < 0:
        return 0
    else:
        return value


class RestAPI(BaseHTTPRequestHandler):
    # https://stackoverflow.com/questions/55764440/python-http-simple-server-persistent-connections
    # https://anshu-dev.medium.com/creating-a-python-web-server-from-basic-to-advanced-449fcb38e93b
    # https://docs.python.org/3/library/http.server.html#module-http.server

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Connection', 'keep-alive')
        self.send_header('keep-alive', 'timeout=5, max=30')
        self.end_headers()

    def do_GET(self):
        global absolute_step
        global benchmark_house
        global decision_house
        global weather
        global cache

        url = urlparse(self.path)
        parameters = parse_qs(url.query)
        print(parameters)

        if url.path == '' or url.path == '/':
            self.path = '/index.html'
        if self.path == '/index.html':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b'Hello, World!')
        elif url.path == '/step':
            if absolute_step == 0:
                self.send_unprocessable_entity()
                return

            if 'lookback' in parameters:
                lookback = parameters['lookback']
                if len(parameters['lookback']) != 1:
                    self.send_unprocessable_entity()
                    return
                try:
                    lookback = int(lookback[0])
                except ValueError:
                    self.send_unprocessable_entity()
                    return

                if lookback > cache_size or lookback > absolute_step:
                    self.send_unprocessable_entity()
                else:
                    self.send_json(cache[len(cache) - lookback:])
                    # self.serial_control(cache[len(cache) - 1])

            else:
                response = cache[len(cache) - 1]
                self.send_json(response)
                # if response['step'] % 6 == 0:
                self.serial_control(response)

    def send_json(self, data):
        response_data = json.dumps(data, cls=SIEncoder).encode('utf-8')
        self.send_response(200)
        self.send_header("Connection", "keep-alive")
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(response_data)))
        self.end_headers()
        self.wfile.write(response_data)

    def do_POST(self):
        global absolute_step
        global benchmark_house
        global decision_house
        global cache
        url = urlparse(self.path)
        parameters = parse_qs(url.query)
        body = {}

        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            if content_length > 0:
                body = self.rfile.read(content_length)
                body = json.loads(body)

        if url.path == '/reset':
            setup()
            self.send_empty_response()

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "PATCH")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.end_headers()

    def do_PATCH(self):
        global absolute_step
        global benchmark_house
        global decision_house
        global cache
        url = urlparse(self.path)
        parameters = parse_qs(url.query)
        body = {}

        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            if content_length > 0:
                body = self.rfile.read(content_length)
                body = json.loads(body)

        if url.path == '/environment':
            if 'outer_temperature' in body.keys():
                benchmark_house.patch_outer_temperature(body['outer_temperature'])
                decision_house.patch_outside_temperature(body['outer_temperature'])

                self.send_empty_response()
                return

        if url.path == '/step':
            diff = 1
            if 'absolute' in body.keys():
                print(body)
                diff = body['absolute'] - absolute_step
                if diff <= 0:
                    self.send_unprocessable_entity()
                    return

            if diff > 144:
                print()
            for i in range(diff):
                step = absolute_step % 144
                month = absolute_step % (144 * 30)
                if diff > 144 and month == 0:
                    print('\r', weather['dates'][absolute_step], end='')
                response = {
                    'step': step,
                    'absolute_step': absolute_step,
                    'environment': {},
                    'benchmark': {},
                    'decision': {}
                }
                for condition in weather.keys():
                    response['environment'][condition] = weather[condition][absolute_step]
                    if condition == 'temperatures':
                        response['environment']['temperatures'] = Temperature.from_celsius(response['environment']['temperatures'])

                benchmark = benchmark_house.step(step, absolute_step, Algorithms.BENCHMARK, weather, DebugLevel.INFORMATIONAL)
                decision = decision_house.step(step, absolute_step, Algorithms.DECISION_TREE, weather, DebugLevel.INFORMATIONAL)

                response['benchmark'] = benchmark
                response['decision'] = decision

                cache.append(response)

                absolute_step += 1
                if len(cache) > cache_size:
                    cache.pop(0)
            if diff > 144:
                print()

            self.send_empty_response()

    def send_unprocessable_entity(self):
        self.send_response(HTTPStatus.UNPROCESSABLE_ENTITY)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(0))
        self.end_headers()

    def send_empty_response(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(0))
        self.end_headers()

    @staticmethod
    def mapper(x: float, in_min: float, in_max: float, out_min: float, out_max: float):
        return abs((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def peaks(self, strip: Strips, value: float):
        if strip in maxi_value.keys():
            if value > maxi_value[strip]:
                maxi_value[strip] = value
        else:
            maxi_value[strip] = value
        if strip in mini_value.keys():
            if value < mini_value[strip]:
                mini_value[strip] = value
        else:
            mini_value[strip] = value

    def send_info(self, strip: Strips, color: Colors, value: float):
        self.write_read(f'{strip:2};{color:2};{trim(value):.3f}\n')  # TODO trim negative, negative transmission

    def serial_control(self, response: dict):
        if response['absolute_step'] % (144 * 30) == 0:
            print(maxi_value)
            print(mini_value)

        sell = response['benchmark']['grid']['sell'].value
        buy = response['benchmark']['grid']['buy'].value
        value = self.mapper(sell - buy, Energy.from_watt_hours(10).value, Energy.from_watt_hours(5).value, -1, 1)
        self.peaks(Strips.GRID, sell - buy)
        self.send_info(Strips.GRID, Colors.MAGENTA if value > 0 else Colors.BLACK, value)

        value = self.mapper(response['benchmark']['battery']['diff'].value, Energy.from_watt_hours(10).value, Energy.from_watt_hours(5).value, -1, 1)
        self.peaks(Strips.BATTERY, response['benchmark']['battery']['diff'].value)
        self.send_info(Strips.BATTERY, Colors.GREEN if value > 0 else Colors.RED, value)
        for generator in response['benchmark']['generators']:
            if generator['name'] == 'Windturbine':
                value = self.mapper(generator['supply'].value, 0, Energy.from_watt_hours(5).value, 1, 0)
                self.peaks(Strips.WIND_TURBINE, generator['supply'].value)
                self.send_info(Strips.WIND_TURBINE, Colors.LIME, value)
            elif generator['name'] == 'SolarPanel':
                value = self.mapper(generator['supply'].value, 0, Energy.from_watt_hours(1000).value, 1, 0)
                self.peaks(Strips.SOLAR_PANEL, generator['supply'].value)
                self.send_info(Strips.SOLAR_PANEL, Colors.LIME, value)
            elif generator['name'] == 'SolarThermal':
                value = self.mapper(generator['supply'].value, 0, Energy.from_watt_hours(1000).value, 1, 0)
                self.peaks(Strips.SOLAR_THERMAL_WATER, generator['supply'].value)
                self.send_info(Strips.SOLAR_THERMAL_WATER, Colors.LIME, value)
        room_demand = []
        room_radiator = []
        for i, room in enumerate(response['benchmark']['rooms']):
            sum = Energy(0)
            for appliance in room['appliances']:
                sum += appliance['demand']
            room_demand.append(sum)
            room_radiator.append(room['radiator'])
        # TODO
        cumulative = Energy(0)
        radiator = False
        room_index = 0
        for i in range(len(room_demand) - 1, 0, -1):  # 0 is on purpose as there is no FIRST UP
            value = self.mapper(room_demand[i].value, 0, Energy.from_watt_hours(5).value, 1, 0)
            self.peaks(Strips.ATTIC_RIGHT + room_index, room_demand[i].value)
            self.send_info(Strips.ATTIC_RIGHT + room_index, Colors.YELLOW, value)
            cumulative += room_demand[i]
            if room_radiator[i]:
                radiator = True
            room_index += 1
            if i % 2 == 0:
                value = self.mapper(cumulative.value, 0, Energy.from_watt_hours(5).value, 1, 0)
                self.peaks(Strips.ATTIC_RIGHT + room_index, cumulative.value)
                self.send_info(Strips.ATTIC_RIGHT + room_index, Colors.YELLOW, value)
                # cumulative = Energy(0)
                value = 0.5
                self.peaks(Strips.THIRD_RADIATORS - (6 - room_index), 0.5)
                self.send_info(Strips.THIRD_RADIATORS - (6 - room_index), Colors.RED, value)
                # radiator = False  # does not make sense as there is no energy flow in between otherwise
                room_index += 1
        value = self.mapper(response['benchmark']['HeatPump']['demand'].value, Energy.from_watt_hours(6).value, Energy.from_watt_hours(5).value, 1, 0)
        self.peaks(Strips.HEATPUMP, response['benchmark']['HeatPump']['demand'].value)
        self.send_info(Strips.HEATPUMP, Colors.RED, value)


    def write_read(self, x):
        if not arduino_found:
            return 'Unable to send'
        transfer = bytes(x, 'utf-8')
        print(f"Sending \"{transfer}\"")
        arduino.write(transfer)
        # time.sleep(0.05)
        # data = arduino.readline()
        return 'Send'


def setup():
    global benchmark_house
    global decision_house
    global weather
    global cache
    cache = []
    benchmark_house = utils.get_house()
    decision_house = utils.get_house()

    benchmark_house.solarPanel.save_weather(weather['radiations'])
    benchmark_house.windturbine.save_weather(weather['winds'], weather['wind_directions'])
    benchmark_house.solarThermal.save_weather(weather['radiations'])
    decision_house.solarPanel.save_weather(weather['radiations'])
    decision_house.windturbine.save_weather(weather['winds'], weather['wind_directions'])
    decision_house.solarThermal.save_weather(weather['radiations'])

    benchmark_house.solarThermal.input_water(Length.from_litre(1_000_000), Temperature.from_celsius(7))
    decision_house.solarThermal.input_water(Length.from_litre(1_000_000), Temperature.from_celsius(7))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), RestAPI)
    # logging.basicConfig(level=logging.DEBUG)
    print(f"Server started http://{hostName}:{serverPort}")

    setup()

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

# Successful until: 3 - 18:40:00 - 23.2.2021
