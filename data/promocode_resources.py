from flask import abort, jsonify
from flask_restful import reqparse, abort, Resource


from . import db_session
from .promocodes import Promocode
from .api_config import abort_if_invalid_api_key


def abort_if_promocode_not_found(promocode_id):
    session = db_session.create_session()
    promocode = session.query(Promocode).get(promocode_id)
    if not promocode:
        abort(404, message=f'Promocode {promocode_id} not found')


class PromocodeResource(Resource):
    def delete(self, promocode_id, api_key):
        abort_if_invalid_api_key(api_key)
        abort_if_promocode_not_found(promocode_id)
        session = db_session.create_session()
        promocode = session.query(Promocode).get(promocode_id)
        session.delete(promocode)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('content', required=True)
parser.add_argument('award', required=True, type=int)


class PromocodeListResource(Resource):
    def post(self, api_key):
        abort_if_invalid_api_key(api_key)
        args = parser.parse_args()
        session = db_session.create_session()
        promocode = Promocode(
            award=args['award']
        )
        if 'id' in args:
            if session.query(Promocode).filter(
                    Promocode.id == args['id']).first():
                return jsonify({'error': 'id already exists'})
            promocode.id = args['id']
        promocode.set_content(args['content'])
        session.add(promocode)
        session.commit()
        return jsonify({'success': 'OK'})
