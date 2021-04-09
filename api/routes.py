import json
from flask import Blueprint, request, make_response
from api.database import db_session
from api.models import Url
from api.methods import generate_hash, generate_hash_with_id


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
        # Crate new URL instance and add to db
        new_url = Url(
            long_url=long_url
        )
        db_session.add(new_url)
        db_session.commit()
        print(new_url.serialize())

        # Create new hash using new URL's id and update instance
        new_hash = generate_hash_with_id(new_url.id)
        new_url.hash = new_hash
        print(new_url.serialize())
        db_session.add(new_url)
        db_session.commit()

        # Serialize instance
        serialized_data = new_url.serialize()

        # Return serialized data
        return make_response(json.dumps(serialized_data), 201)

    return 'short url'


@api.route('/redirect-url', methods=['GET'])
def redirect_url():
    print(request)
    return 'redirect url'


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
        new_url = Url(long_url=long_url, hash='shortio')
        db_session.add(new_url)
        db_session.commit()

        return json.dumps(new_url.short_url)

    return 'Error'
