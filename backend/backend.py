import json
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import utils
from DebugLevel import DebugLevel
from House import House
from Physics import SIEncoder

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
        global weather
        global cache

        url = urlparse(self.path)
        #print(url)
        parameters = parse_qs(url.query)
        print(parameters)

        if url.path == '' or url.path == '/':
            self.path = '/index.html'
        if self.path == '/index.html':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b'Hello, World!')
            # self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            # self.wfile.write(bytes("<body>", "utf-8"))
            # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            # self.wfile.write(bytes("</body></html>", "utf-8"))
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

        # print(f'{self.client_address=}')  # ('127.0.0.1', 40972)
        # print(f'{self.requestline=}')  # POST / HTTP/1.1
        # print(f'{self.command=}')  # POST
        # print(f'{self.path=}')  # '/'
        # print(f'{self.headers=}')  # <http.client.HTTPMessage object at 0x7f2a0660f110>
        # print(f'{self.rfile=}')  # <_io.BufferedReader name=4>
        # print(f'{self.wfile=}')

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        curr_time = datetime.now()
        # response_data = b'{"msgid": 1234}'
        # data = f'{{"msgid": {str(msg_id)}, "time": "{str(curr_time)}"}}'
        data = {"msgid": str(absolute_step), "time": str(curr_time)}
        response_data = json.dumps(data).encode('utf-8')

        # Send the response
        self.send_response(200)
        self.send_header("Connection", "keep-alive")
        self.send_header("Content-Length", str(len(response_data)))
        self.end_headers()

        # Write _exactly_ the number of bytes specified by the
        # 'Content-Length' header
        self.wfile.write(response_data)
        absolute_step += 1

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
        global cache
        url = urlparse(self.path)
        parameters = parse_qs(url.query)
        # print(self.path)
        # print(self.command, url)
        # print(self)
        # print(self.headers)
        body = {}

        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            if content_length > 0:
                body = self.rfile.read(content_length)
                body = json.loads(body)
                # print(body)

        if url.path == '/environment':
            if 'outer_temperature' in body.keys():
                benchmark_house.patch_outer_temperature(body['outer_temperature'])

                self.send_empty_response()
                return

        if url.path == '/step':
            diff = 1
            if 'absolute' in body.keys():
                print(body)
                diff = body['absolute'] - absolute_step
                # print(diff)
                if diff <= 0:
                    self.send_unprocessable_entity()
                    return

            for i in range(diff):
                step = absolute_step % 144
                response = {
                    'step': step,
                    'absolute_step': absolute_step,
                    'environment': {},
                    'benchmark': {},
                    'decision': {}
                }
                for condition in weather.keys():
                    response['environment'][condition] = weather[condition][absolute_step]

                benchmark = benchmark_house.step(step, absolute_step, House.Algorithms.BENCHMARK, weather, DebugLevel.INFORMATIONAL)
                decision = decision_house.step(step, absolute_step, House.Algorithms.DECISION_TREE, weather, DebugLevel.INFORMATIONAL)

                response['benchmark'] = benchmark
                response['decision'] = decision

                cache.append(response)

                absolute_step += 1
                # print(len(cache))
                if len(cache) > cache_size:
                    cache.pop(0)

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


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), RestAPI)
    # logging.basicConfig(level=logging.DEBUG)
    print(f"Server started http://{hostName}:{serverPort}")

    benchmark_house.solarPanel.save_weather(weather['radiations'])
    benchmark_house.windturbine.save_weather(weather['winds'], weather['wind_directions'])

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

# Successful until: 3 - 18:40:00 - 23.2.2021
