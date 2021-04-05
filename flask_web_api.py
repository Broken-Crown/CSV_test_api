from flask import Flask
from flask_restful import Resource, Api, reqparse
import data

app = Flask(__name__)
api = Api(app)


class Product(Resource):
    """
    need to have only one endpoint that will takes to args
    TestMe: http://127.0.0.1:5000/product?sku=WP260qJAo6&rank=0.9
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("sku",required=True)
        parser.add_argument("rank",required=False)

        args = parser.parse_args()

        result = data.get_rec_sku_csv(args['sku'],args['rank'])

        return result, 200


api.add_resource(Product,'/product')


if __name__ == '__main__':
    app.run()