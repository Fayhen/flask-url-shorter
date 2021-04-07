from flask import Blueprint, request
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
