# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
import json

from model.PhishingModel import PhishingModel
from urllib import parse



hostName = "localhost"
serverPort = 5000


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        model = PhishingModel()
        query_components = dict(parse.parse_qsl(parse.urlsplit(self.path).query))

        test_data = [query_components['text_link_disparity'],
                     query_components['re_mail'],
                     query_components['urls'],
                     query_components['body_richness'],
                     query_components['contains_prime_targets'],
                     query_components['contains_account'],
                     query_components['domains'],
                     query_components['HTML'],
                     query_components['malicious_urls'],
                     query_components['ip_urls'],
                     query_components['attachments'],
                     query_components['dots_count'],
                     query_components['hex_urls'],
                     query_components['mailto'],
                     query_components['contains_update'],
                     query_components['contains_access']]

        predict = model.predict(np.array([test_data])).tolist()[0]

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(bytes(json.dumps({'result': predict}), 'utf-8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")