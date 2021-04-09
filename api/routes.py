import json
from flask import Blueprint, request, redirect, make_response
from api.database import db_session
from api.models import Url
from api.methods import generate_hash_with_id, get_full_url
from api.validators import validate_url


api = Blueprint('api', __name__, url_prefix='/lil')


@api.route('/hello')
def hello():
    return 'Hello, World!'


@api.route('/short-url', methods=['POST'])
def short_url():
    print(request.url_root)
    data = request.json
    long_url = data.get('url', None)
    valid = validate_url(str(long_url))

    if long_url and valid:
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

    error_msg = 'Sorry, we couldn\'t shorten the URL. Please ensure the URL begins' \
                ' with \'https://\' or \'http://\', and has a valid format. Examples:' \
                ' \'https://my-url.com\', \'https://www.my-url.com\'.'

    return make_response({"error": error_msg}, 400)


@api.route('/<string:hashed_id>', methods=['GET'])
def redirect_url(hashed_id):
    """
    Redirection route. Redirects request to a short URL to the
    full URL.
    """
    url = get_full_url(hashed_id)
    print(url)
    print(bool(url))
    if url:
        print("fired if")
        return redirect(url)

    return 'redirect url'


@api.route('get-db', methods=['GET'])
def get_db():
    """
    Dev route. Returns all URLs in database.
    """
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
