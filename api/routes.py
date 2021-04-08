import json
from flask import Blueprint, request
from api.database import db, Url
from api.methods import hash_url


api = Blueprint('api', __name__, url_prefix='/lil')


@api.route('/hello')
def hello():
    return 'Hello, World!'


@api.route('/short-url', methods=['POST'])
def short_url():
    print(request.url_root)
    data = request.json
    long_url = data.get('url', None)
    if long_url is not None:
        hashed = hash_url(long_url)
        print(hashed)
    return 'short url'


@api.route('/redirect-url', methods=['GET'])
def redirect_url():
    print(request)
    return 'redirect url'


@api.route('/try_db', methods=['GET'])
def try_db():
    print(request)
    urls = Url.query.all()
    print(urls)
    return 'try_db'


@api.route('get-db', methods=['GET'])
def get_db():
    urls = Url.query.all()
    print(urls)
    return json.dumps(Url.serialize_list(urls))


@api.route('post-db', methods=['POST'])
def post_db():
    data = request.json
    long_url = data.get('url', None)
    if long_url is not None:
        new_url = Url(long_url=long_url, short_url='shortio')
        db.session.add(new_url)
        db.session.commit()

        return json.dumps(new_url.short_url)

    return 'Error'
