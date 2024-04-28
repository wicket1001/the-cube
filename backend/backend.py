import json
import logging
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from io import BytesIO
from urllib.parse import urlparse, parse_qs

import utils
from DebugLevel import DebugLevel
from House import House
from Physics import SIEncoder

hostName = "localhost"
serverPort = 8080


msg_id = 1
house = House()
weather = utils.read_csv(DebugLevel.INFORMATIONAL)


class RestAPI(BaseHTTPRequestHandler):
    # https://stackoverflow.com/questions/55764440/python-http-simple-server-persistent-connections
    # https://anshu-dev.medium.com/creating-a-python-web-server-from-basic-to-advanced-449fcb38e93b

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Connection', 'keep-alive')
        self.send_header('keep-alive', 'timeout=5, max=30')
        self.end_headers()

    def do_GET(self):
        global msg_id
        global house
        global weather

        url = urlparse(self.path)
        print(url)
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
            response = house.step(msg_id, msg_id, weather, DebugLevel.INFORMATIONAL)
            response_data = json.dumps(response, cls=SIEncoder).encode('utf-8')

            self.send_response(200)
            self.send_header("Connection", "keep-alive")
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", str(len(response_data)))
            self.end_headers()

            # Write _exactly_ the number of bytes specified by the
            # 'Content-Length' header
            self.wfile.write(response_data)
            msg_id += 1

    def do_POST(self):
        global msg_id

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
        data = {"msgid": str(msg_id), "time": str(curr_time)}
        response_data = json.dumps(data).encode('utf-8')

        # Send the response
        self.send_response(200)
        self.send_header("Connection", "keep-alive")
        self.send_header("Content-Length", str(len(response_data)))
        self.end_headers()

        # Write _exactly_ the number of bytes specified by the
        # 'Content-Length' header
        self.wfile.write(response_data)
        msg_id += 1

    # def do_PATCH(self):
    #     pass


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), RestAPI)
    # logging.basicConfig(level=logging.DEBUG)
    print(f"Server started http://{hostName}:{serverPort}")

    house.solarPanel.save_weather(weather['radiations'])
    house.windturbine.save_weather(weather['winds'], weather['wind_directions'])

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
