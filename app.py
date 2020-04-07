from flask import Flask

from data import db_session
from data.users import User
from data.products import Product
from data.categories import Category



app = Flask(__name__)
app.config['SECRET_KEY'] = '474B70726F64756374696F6E5F3533637233375F6B3379'


@app.route('/')
def index():
    return '11233'


def main():
    db_session.global_init('db/GK-store.sqlite')

    app.run(debug=True)


if __name__ == '__main__':
    main()
