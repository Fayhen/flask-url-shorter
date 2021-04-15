import json
from flask import Blueprint, request, redirect, make_response, g, current_app
# from api.database import db_session
from api import db
from api.models import Url
from api.methods import generate_hash, get_url_by_hash
from api.validators import validate_url


api = Blueprint('api', __name__, url_prefix='/lil')


@api.route('/shorten-url', methods=['POST'])
def add_url():
    data = request.json
    long_url = data.get('url', None) if data else None
    valid = validate_url(str(long_url))

    if long_url and valid:
        # Crate new URL instance and add to db
        new_url = Url(
            long_url=long_url
        )
        db.session.add(new_url)
        db.session.commit()

        # Create new hash using new URL's id and update instance
        new_hash = generate_hash(new_url.id)
        new_url.hash = new_hash
        db.session.add(new_url)
        db.session.commit()

        data = {
            'short_url': f'{request.url_root}lil/{new_url.hash}'
        }

        return make_response(data, 201)

    error_msg = 'Sorry, we couldn\'t shorten the URL. Please ensure the URL begins' \
                ' with \'https://\' or \'http://\', and has a valid format. Examples:' \
                ' \'https://my-url.com\', \'https://www.my-url.com\'.'

    return make_response({'error': error_msg}, 400)


@api.route('/<string:hashed_id>', methods=['GET', 'DELETE'])
def redirect_url(hashed_id):
    """
    Short URL handler. Redirects short URLs to their full address counterpart on
    GET requests. Deletes short URLs on DELETE requests.
    """
    url = get_url_by_hash(hashed_id)

    # GET requests handler
    if url and request.method == 'GET':
        # Increment URL access counter before redirecting
        url.clicks = url.clicks + 1
        db.session.add(url)
        db.session.commit()

        return redirect(url.long_url)

    # DELETE requests handler
    if url and request.method == 'DELETE':
        db.session.delete(url)
        db.session.commit()

        return make_response({'msg': 'URL deleted.'}, 200)

    error_msg = 'Sorry, the requested short URL was not found.'
    return make_response({'error': error_msg}, 404)


@api.route('/<string:hashed_id>/clicks', methods=['GET'])
def get_clicks(hashed_id):
    """
    Click counting route. Returns how many times a short URL was
    visited.
    """
    url = get_url_by_hash(hashed_id)
    if url:
        data = {
            'clicks': url.clicks,
            'message': f'This short URL has been accessed {url.clicks} times.'
        }

        return make_response(data, 200)

    error_msg = 'Sorry, the requested short URL was not found.'
    return make_response({'error': error_msg}, 404)


@api.route('get-all', methods=['GET'])
def get_all():
    """
    Dev route. Returns all URLs in database.
    """
    urls = Url.query.all()

    return json.dumps(Url.serialize_list(urls))
