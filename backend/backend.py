import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import utils
from DebugLevel import DebugLevel
from Physics import SIEncoder, Temperature, Length
from algorithm_utils import Algorithms

hostName = "localhost"
serverPort = 8080


absolute_step = 0
benchmark_house = utils.get_house()
decision_house = utils.get_house()
weather = utils.read_csv(DebugLevel.INFORMATIONAL)
cache = []
cache_size = 72


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

            else:
                self.send_json(cache[len(cache) - 1])

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
                if diff > 144 and step == 0:
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
