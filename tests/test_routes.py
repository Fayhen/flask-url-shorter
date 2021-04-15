import json
from api.models import Url
from api.methods import generate_hash


def test_add_url_with_valid_data(client):
    valid_data = {'url': 'https://github.com'}
    response = client.post('/lil/shorten-url', json=valid_data)

    assert response.status_code == 201
    assert 'short_url' in json.loads(response.data)


def test_add_url_with_invalid_data(client):
    no_https = {'url': 'github.com'}
    https_typo = {'url': 'htsp://github.com'}
    empty_string = {'url': ''}

    response_no_https = client.post('/lil/shorten-url', json=no_https)
    response_typo_https = client.post('/lil/shorten-url', json=https_typo)
    response_empty_string = client.post('/lil/shorten-url', json=empty_string)
    response_no_data = client.post('/lil/shorten-url')

    assert response_no_https.status_code == 400
    assert response_typo_https.status_code == 400
    assert response_empty_string.status_code == 400
    assert response_no_data.status_code == 400

    assert 'error' in json.loads(response_no_https.data)
    assert 'error' in json.loads(response_typo_https.data)
    assert 'error' in json.loads(response_empty_string.data)
    assert 'error' in json.loads(response_no_data.data)


def test_add_url_wrong_http_methods(client):
    get_response = client.get('/lil/shorten-url')
    put_response = client.put('/lil/shorten-url')
    patch_response = client.patch('/lil/shorten-url')
    delete_response = client.delete('/lil/shorten-url')

    assert get_response.status_code == 404
    assert put_response.status_code == 405
    assert patch_response.status_code == 405
    assert delete_response.status_code == 404


def test_redirect(client):
    create_url_response = client.post('/lil/shorten-url', json={'url': 'https://github.com'})
    new_url = json.loads(create_url_response.data).get('short_url', None)

    request_short_url_response = client.get(new_url)
    print(request_short_url_response)

    assert new_url is not None
    assert request_short_url_response.status_code == 302


# def test_redirect2(client, db):
#     new_url = Url(long_url='https://github.com')
#     db.session.add(new_url)
#     db.session.commit()
#
#     new_url.hash = generate_hash(new_url.id)
#     db.session.add(new_url)
#     db.session.commit()
#
#     request_short_url_response = client.get(f'/lil/{new_url.hash}')
#     assert request_short_url_response.status_code == 302
