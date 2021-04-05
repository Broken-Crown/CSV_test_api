from http.server import HTTPServer, BaseHTTPRequestHandler
import main
import os


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
            return
        if '?' not in endpoint:
            self.end_headers()
            self.wfile.write(bytes("Please, choose at least sku, rank is optional", 'utf-8'))
            return
        args = endpoint.split('?')[1].split('&')

        for arg in args:
            if "sku" in arg:
                sku = arg.split('=')[1]
            elif "rank" in arg:
                rank = arg.split('=')[1]
        if isinstance(sku,type(None)):
            self.end_headers()
            self.wfile.write(bytes("Sorry, but sku is obligatory, rank is optional", 'utf-8'))
            return
        result = main.find_some_row(sku, rank)
        self.end_headers()
        self.wfile.write(bytes(f"{result}", 'utf-8'))
        return


if __name__ == '__main__':
    if os.path.isdir(".\\tmp") is False:
        os.mkdir('.\\tmp')
    if os.path.isdir(".\\tmp\\test") is False:
        os.mkdir(".\\tmp\\test")

    new_scv_name = 'new_recommends.csv'
    if os.path.isfile(f".\\tmp\\{new_scv_name}") is False:
        main.create_dict_from_csv()

    main.csv_separator()

    server = HTTPServer(('127.0.0.1', 5000), ServiceHandler)
    server.serve_forever()
