from flask import abort, jsonify
from flask_restful import reqparse, abort, Resource


from . import db_session
from .users import User
from .api_config import abort_if_invalid_api_key


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')


class UserResource(Resource):
    def get(self, user_id, api_key):
        abort_if_invalid_api_key(api_key)
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'User': user.to_dict(
            only=('name', 'surname', 'about', 'phone_number',
                  'email', 'balance', 'permission', 'sum_rating',
                  'count_rating', 'created_date'))})

    def delete(self, user_id, api_key):
        abort_if_invalid_api_key(api_key)
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        for product in user.products:
            if not product.is_sold:
                session.delete(product)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('name', required=True)
parser.add_argument('surname')
parser.add_argument('about')
parser.add_argument('phone_number')
parser.add_argument('email', required=True)
parser.add_argument('permission', required=True)
parser.add_argument('password', required=True)
parser.add_argument('avatar_source')


class UserListResource(Resource):
    def get(self, api_key):
        abort_if_invalid_api_key(api_key)
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'Users': [item.to_dict(
            only=('name', 'surname', 'email',
                  'balance', 'permission')) for item in users]})

    def post(self, api_key):
        abort_if_invalid_api_key(api_key)
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.email == args['email']).first():
            return jsonify({'error': 'email already exists'})
        user = User(
            name=args['name'],
            email=args['email'],
            permission=args['permission']
        )
        if 'id' in args:
            if session.query(User).filter(User.id == args['id']).first():
                return jsonify({'error': 'id already exists'})
            user.id = args['id']
        if 'surname' in args:
            user.surname = args['surname']
        if 'about' in args:
            user.about = args['about']
        if 'phone_number' in args:
            user.phone_number = args['phone_number']
        if 'avatar_source' in args:
            user.avatar_source = args['avatar_source']
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
