from flask import abort, jsonify
from flask_restful import reqparse, abort, Resource


from . import db_session
from .transactions import Transaction
from .users import User
from .products import Product
from .users import User
from .api_config import abort_if_invalid_api_key


def abort_if_transaction_not_found(transaction_id):
    session = db_session.create_session()
    transaction = session.query(Transaction).get(transaction_id)
    if not transaction:
        abort(404, message=f'Transaction {transaction_id} not found')


class TransactionResource(Resource):
    def get(self, transaction_id, api_key):
        abort_if_invalid_api_key(api_key)
        abort_if_transaction_not_found(transaction_id)
        session = db_session.create_session()
        transaction = session.query(Transaction).get(transaction_id)
        return jsonify({'Transaction': transaction.to_dict(
            only=('seller_id', 'buyer_id', 'product_id', 'status',
                  'date', 'price'))})

    def delete(self, transaction_id, api_key):
        abort_if_invalid_api_key(api_key)
        abort_if_transaction_not_found(transaction_id)
        session = db_session.create_session()
        transaction = session.query(Transaction).get(transaction_id)
        session.delete(transaction)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('seller_id', required=True, type=int)
parser.add_argument('buyer_id', required=True, type=int)
parser.add_argument('product_id', required=True, type=int)


class TransactionListResource(Resource):
    def get(self, api_key):
        abort_if_invalid_api_key(api_key)
        session = db_session.create_session()
        transactions = session.query(Transaction).all()
        return jsonify({'Transactions': [item.to_dict(
            only=('seller_id', 'buyer_id', 'product_id',
                  'status', 'date', 'price')) for item in transactions]})

    def post(self, api_key):
        abort_if_invalid_api_key(api_key)
        args = parser.parse_args()
        session = db_session.create_session()
        transaction = Transaction(
            seller_id=args['seller_id'],
            buyer_id=args['buyer_id'],
            product_id=args['product_id']
        )
        if 'id' in args:
            if session.query(Transaction).filter(
                    Transaction.id == args['id']).first():
                return jsonify({'error': 'id already exists'})
            transaction.id = args['id']
        product = session.query(Product).get(args['product_id'])
        buyer = session.query(User).get(args['buyer_id'])
        seller = session.query(User).get(args['seller_id'])
        if buyer.balance < product.price:
            return jsonify({'error': 'insufficient funds'})
        transaction.status = 'Куплено'
        product.is_sold = True
        buyer.balance -= product.price
        seller.balance += product.price * 0.95
        admin = session.query(User).filter(User.permission == 'admin').first()
        admin.balance += product.price * 0.05
        transaction.price = product.price
        session.add(transaction)
        session.commit()
        return jsonify({'success': 'OK'})
