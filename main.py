""" Simple Dummy Server """
from __future__ import annotations
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
from typing import Type, TypeVar


def get_response_body(filename: str):
    """ get response body. """
    res_body = open(filename)
    return res_body.read()


MyHandler = TypeVar('MyHandler', bound='MyHTTPRequestHandler')


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """ Dummy Web sevrer class. """
    response_file: str = ""

    @classmethod
    def generate_handler(cls: Type[MyHandler],
                         response_file: str) -> Type[MyHandler]:
        """ return HTTPRequestHandler. """
        cls.response_file = response_file

        return cls

    def do_GET(self):  # TODO: add type.
        """ return the http response when it receives the GET request. """
        response_body = get_response_body(self.response_file)

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.send_header('Content-length', len(response_body))
        self.end_headers()
        self.wfile.write(response_body.encode('utf-8'))
        logging.info('[Request method] GET')
        logging.info("[Request headers]\n%s", str(self.headers))

    def do_POST(self):
        """ return the http response when it receives the POST request. """
        response_body = get_response_body("index.html")

        self.send_response(200)
        self.send_header('Content-type', 'text/xml; charset=UTF-8')
        self.send_header('Content-length', len(response_body))
        self.end_headers()
        self.wfile.write(response_body)
        logging.info('[Request method] POST')
        logging.info("[Request headers]\n%s", str(self.headers))

        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        logging.info('[Request doby]\n%s', post_body)


def parse_args():
    """ parse args """
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--res', type=str, default='index.html')

    args = parser.parse_args()

    return args.port, args.res


def main():
    """ main """
    host = ''
    port, res = parse_args()
    handler = MyHTTPRequestHandler.generate_handler(res)
    httpd = HTTPServer((host, port), handler)

    logging.info('Server Starting...')
    logging.info('Listening at port :%d', port)

    try:
        httpd.serve_forever()
    except BaseException:
        logging.info('Server Stopped')


if __name__ == '__main__':
    main()
