from flask import abort, jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .products import Product
from .api_config import abort_if_invalid_api_key


def abort_if_product_not_found(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if not product:
        abort(404, message=f'Product {product_id} not found')


class ProductResource(Resource):
    def get(self, product_id, api_key):
        abort_if_invalid_api_key(api_key)
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        return jsonify({'product': product.to_dict(
            only=('title', 'short_about', 'about', 'price',
                  'user_id', 'is_published', 'created_date'))})

    def delete(self, product_id, api_key):
        abort_if_invalid_api_key(api_key)
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        session.delete(product)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('title', required=True)
parser.add_argument('short_about', required=True)
parser.add_argument('about', required=True)
parser.add_argument('image_source')
parser.add_argument('price', required=True, type=float)
parser.add_argument('purchased_content', required=True)
parser.add_argument('is_published', type=bool)
parser.add_argument('user_id', required=True, type=int)


class ProductListResource(Resource):
    def get(self, api_key):
        abort_if_invalid_api_key(api_key)
        session = db_session.create_session()
        products = session.query(Product).all()
        return jsonify({'products': [item.to_dict(
            only=('title', 'short_about',
                  'price', 'user_id')) for item in products]})

    def post(self, api_key):
        abort_if_invalid_api_key(api_key)
        args = parser.parse_args()
        session = db_session.create_session()
        product = Product(
            title=args['title'],
            short_about=args['short_about'],
            about=args['about'],
            price=args['price'],
            user_id=args['user_id'],
            purchased_content=args['purchased_content']
        )
        if 'id' in args:
            product.id = args['id']
        if 'image_source' in args:
            product.image_source = args['image_source']
        if 'is_published' in args:
            product.is_published = args['is_published']
        session.add(product)
        session.commit()
        return jsonify({'success': 'OK'})
