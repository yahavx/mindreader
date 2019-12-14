import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import re


class Website:
    paths = {}
    response_404 = '''
    <html>
        <head>
            <title>Error 404 (page not found)</title>
        </head>
        <body>
            Error 404: page not found.
        </body>
    </html>
    '''

    def route(self, path):
        def decorator(f):
            Website.paths[re.compile(path)] = f
            return f
        return decorator

    def run(self, address):
        httpd = HTTPServer(address, Serv)
        httpd.serve_forever()


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        pattern = next((path for path in Website.paths if re.search(path, self.path) is not None), None)  # find a matching RE
        match = re.search(pattern, self.path)

        if pattern is None or match.span()[1] - match.span()[0] != len(self.path):  # no matching pattern to current request
            self.send_response(404)
            self.end_headers()
            # self.wfile.write(bytes(Website.response_404, 'utf-8'))
            return

        handler = Website.paths[pattern]
        ret = handler(*match.groups())

        if ret[0] == 404:
            self.send_response(404)
            self.end_headers()
            # self.wfile.write(bytes(Website.response_404, 'utf-8'))
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(ret[1], 'utf-8'))
