import json
import math
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import serial

from utils import get_house, read_csv, Strips, Colors, mapper, get_boundaries
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
benchmark_house = get_house()
decision_house = get_house()
weather = read_csv(DebugLevel.INFORMATIONAL)
max_boundaries, min_boundaries = get_boundaries()
cache = []
cache_size = 144


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
                    self.serial_control(cache[len(cache) - 1])

            else:
                response = cache[len(cache) - 1]
                self.send_json(response)
                if response['step'] % 6 == 0:
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

    def send_info(self, strip: Strips, color: Colors, value: (float, Energy), reverse=False):
        if isinstance(value, Energy):
            value = value.value
        if reverse:
            value = 1 - value
        self.write_read(f'{strip:2};{color:2};{trim(value):>6.3f};x\n')  # TODO trim negative, negative transmission

    def serial_control(self, response: dict):
        diff = response['benchmark']['grid']['diff']
        if diff.value < 0:
            pass
            #self.send_info(Strips.GRID, Colors.MAGENTA, diff / min_boundaries[Strips.GRID], True)
        else:
            pass
            #self.send_info(Strips.GRID, Colors.BLACK, diff / max_boundaries[Strips.GRID], True)

        diff = response['benchmark']['battery']['diff']
        if diff.value < 0:
            pass
            # self.send_info(Strips.BATTERY, Colors.GREEN, diff / min_boundaries[Strips.BATTERY], True)
        else:
            pass
            # self.send_info(Strips.BATTERY, Colors.RED, diff / max_boundaries[Strips.BATTERY], True)
        for generator in response['benchmark']['generators']:
            if generator['name'] == 'Windturbine':
                self.send_info(Strips.WIND_TURBINE, Colors.LIME, generator['supply'] / max_boundaries[Strips.WIND_TURBINE], True)
            elif generator['name'] == 'SolarPanel':
                self.send_info(Strips.SOLAR_PANEL, Colors.LIME, generator['supply'] / max_boundaries[Strips.SOLAR_PANEL], True)
            elif generator['name'] == 'SolarThermal':
                pass
                # self.send_info(Strips.SOLAR_THERMAL_WATER, Colors.RED, generator['supply'] / max_boundaries[Strips.SOLAR_THERMAL_WATER], True)
        room_radiator = []
        cumulative = Energy(0)
        radiator = False
        room_index = 0
        demand = response['benchmark']['rooms'][2]['demand']
        self.send_info(Strips.FIRST_LEFT, Colors.YELLOW, demand / max_boundaries[Strips.FIRST_LEFT], True)
        # for i in range(len(response['benchmark']['rooms']) - 1, -1, -1):  # 0 is on purpose as there is no FIRST UP
        #     room_info = response['benchmark']['rooms'][i]
        #     demand = room_info['demand']
        #     index = Strips.ATTIC_RIGHT + room_index
        #     # print(index)
        #     self.send_info(index, Colors.YELLOW, demand / max_boundaries[index], True)
        #     cumulative += demand
        #     if room_info['radiator']:
        #         radiator = True
        #     room_index += 1
        #     if i % 2 == 0:
        #         self.send_info(
        #             Strips.ATTIC_RIGHT + room_index,
        #             Colors.YELLOW,
        #             cumulative / max_boundaries[Strips.ATTIC_RIGHT + room_index],
        #             True
        #         )
        #         # cumulative = Energy(0)
        #         up_radiators = Strips.THIRD_RADIATORS - (6 - math.floor(room_index / 3))
        #         if radiator:
        #             pass
        #             # self.send_info(
        #             #     up_radiators,
        #             #     Colors.RED,
        #             #     0.5,
        #             #     True
        #             # )
        #         else:
        #             pass
        #             # self.send_info(
        #             #     up_radiators,
        #             #     Colors.RED,
        #             #     0,
        #             #     True
        #             # )
        #         # radiator = False  # does not make sense as there is no energy flow in between otherwise
        #         room_index += 1
        #         floor_radiators = Strips.THIRD_RADIATORS - (6 - math.ceil(room_index / 3))
        #         if radiator:
        #             pass
        #             # self.send_info(
        #             #     floor_radiators,
        #             #     Colors.RED,
        #             #     0.5,
        #             #     True
        #             # )
        #         else:
        #             pass
        #             # self.send_info(
        #             #     floor_radiators,
        #             #     Colors.RED,
        #             #     0,
        #             #     True
        #             # )
        # pass
        #self.send_info(Strips.HEATPUMP, Colors.RED, response['benchmark']['HeatPump']['demand'] / max_boundaries[Strips.HEATPUMP], True)


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
    benchmark_house = get_house()
    decision_house = get_house()

    benchmark_house.solarPanel.save_weather(weather['radiations'])
    benchmark_house.windturbine.save_weather(weather['winds'], weather['wind_directions'])
    benchmark_house.solarThermal.save_weather(weather['radiations'], weather['winds'], weather['temperatures'])
    decision_house.solarPanel.save_weather(weather['radiations'])
    decision_house.windturbine.save_weather(weather['winds'], weather['wind_directions'])
    decision_house.solarThermal.save_weather(weather['radiations'], weather['winds'], weather['temperatures'])

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
