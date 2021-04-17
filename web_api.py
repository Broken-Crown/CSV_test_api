from http.server import HTTPServer, BaseHTTPRequestHandler
import searcher
import os

_CSV_DIR_PATH = os.path.abspath(".\\tmp\\separated csv\\")


class ServiceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        sku = None
        rank = None

        self.send_response(200)
        self.send_header('Content-type', 'text')

        get_request = self.requestline
        endpoint = get_request.split('/')[1].split(' ')[0]

        if endpoint == '':
            self.end_headers()
            self.wfile.write(bytes("Hello, we have some products, check it out (example "
                                   "http://127.0.0.1:5000/product?sku=WP260qJAo6&rank=0.9)", 'utf-8'))
            return None

        if '?' not in endpoint:
            self.end_headers()
            self.wfile.write(bytes("Please, choose at least sku, rank is optional", 'utf-8'))

            return None

        args = endpoint.split('?')[1].split('&')

        for arg in args:
            if "sku" in arg:
                sku = arg.split('=')[1]
            elif "rank" in arg:
                rank = arg.split('=')[1]

        if isinstance(sku, type(None)):
            self.end_headers()
            self.wfile.write(bytes("Sorry, but sku is obligatory, rank is optional", 'utf-8'))

            return None

        result = searcher.find_some_row(sku, _CSV_DIR_PATH, rank)
        self.end_headers()
        self.wfile.write(bytes(f"{result}", 'utf-8'))

        return None


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 5000), ServiceHandler)
    server.serve_forever()
