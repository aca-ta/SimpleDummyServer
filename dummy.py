from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import logging
import sys

# Dummy Web sevrer class.
class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        f = open("index.html")
        response_body = f.read()
        print(response_body)

        self.send_response(201)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.send_header('Content-length', len(response_body))
        self.end_headers()
        self.wfile.write(response_body.encode('utf-8'))
        logging.info('[Request method] GET')
        logging.info('[Request headers]\n' + str(self.headers))

    def do_POST(self):
        f = open("index.html")
        response_body = f.read()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/xml; charset=UTF-8')
        self.send_header('Content-length', len(response_body))
        self.end_headers()
        self.wfile.write(response_body)
        logging.info('[Request method] POST')
        logging.info('[Request headers]\n' + str(self.headers))

        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        logging.info('[Request doby]\n' + post_body)



host = ''
port = 8000
httpd = HTTPServer((host, port), MyHTTPRequestHandler)

logging.info('Server Starting...')
logging.info('Listening at port :%d', port)

try:
    httpd.serve_forever()
except:
    logging.info('Server Stopped')
