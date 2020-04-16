from flask import abort, jsonify
from flask_restful import reqparse, abort, Resource


from . import db_session
from .categories import Category
from .api_config import abort_if_invalid_api_key


def abort_if_category_not_found(category_id):
    session = db_session.create_session()
    category = session.query(Category).get(category_id)
    if not category:
        abort(404, message=f'Category {category_id} not found')


class CategoryResource(Resource):
    def get(self, category_id, api_key):
        abort_if_invalid_api_key(api_key)
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        return jsonify({'Category': category.to_dict(only=('name',))})

    def delete(self, category_id, api_key):
        abort_if_invalid_api_key(api_key)
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        session.delete(category)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('name', required=True)


class CategoryListResource(Resource):
    def get(self, api_key):
        abort_if_invalid_api_key(api_key)
        session = db_session.create_session()
        categories = session.query(Category).all()
        return jsonify({'Categories': [item.to_dict(
            only=('name',)) for item in categories]})

    def post(self, api_key):
        abort_if_invalid_api_key(api_key)
        args = parser.parse_args()
        session = db_session.create_session()
        category = Category(
            name=args['name']
        )
        if 'id' in args:
            category.id = args['id']
        session.add(category)
        session.commit()
        return jsonify({'success': 'OK'})