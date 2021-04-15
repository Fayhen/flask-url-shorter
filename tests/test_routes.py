def test_add_url_with_valid_data(client):
    valid_data = {'url': 'https://github.com'}
    response = client.post('/lil/shorten-url', json=valid_data)

    assert response.status_code == 201
    assert 'short_url' in response.get_json()


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

    assert 'error' in response_no_https.get_json()
    assert 'error' in response_typo_https.get_json()
    assert 'error' in response_empty_string.get_json()
    assert 'error' in response_no_data.get_json()


def test_add_url_with_wrong_http_methods(client):
    get_response = client.get('/lil/shorten-url')
    put_response = client.put('/lil/shorten-url')
    patch_response = client.patch('/lil/shorten-url')
    delete_response = client.delete('/lil/shorten-url')

    assert get_response.status_code == 404
    assert put_response.status_code == 405
    assert patch_response.status_code == 405
    assert delete_response.status_code == 404


def test_post_and_redirect(client):
    create_url_response = client.post('/lil/shorten-url', json={'url': 'https://github.com'})
    new_url = create_url_response.get_json().get('short_url', None)

    request_short_url_response = client.get(new_url)
    location = request_short_url_response.headers.get('Location', None)

    assert new_url is not None
    assert location is not None
    assert request_short_url_response.status_code == 302


def test_redirect_with_wrong_http_methods(client):
    create_url_response = client.post('/lil/shorten-url', json={'url': 'https://github.com'})
    new_url = create_url_response.get_json().get('short_url', None)

    post_response = client.post(new_url)
    put_response = client.put(new_url)
    patch_response = client.patch(new_url)

    assert post_response.status_code == 405
    assert put_response.status_code == 405
    assert patch_response.status_code == 405


def test_delete(client):
    create_url_response = client.post('/lil/shorten-url', json={'url': 'https://github.com'})
    new_url = create_url_response.get_json().get('short_url', None)

    delete_response = client.delete(new_url)
    delete_response_data = delete_response.get_json()

    get_deleted_response = client.get(new_url)
    get_deleted_response_data = get_deleted_response.get_json()

    assert new_url is not None
    assert delete_response.status_code == 200
    assert 'msg' in delete_response_data
    assert get_deleted_response.status_code == 404
    assert 'error' in get_deleted_response_data


# def test_redirect(client, db):
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


def test_get_clicks(client):
    create_url_response = client.post('/lil/shorten-url', json={'url': 'https://github.com'})
    new_url = create_url_response.get_json().get('short_url', None)

    clicks_response = client.get(new_url + '/clicks')
    clicks_response_data = clicks_response.get_json()

    assert new_url is not None
    assert clicks_response.status_code == 200
    assert 'clicks' in clicks_response_data
    assert 'msg' in clicks_response_data


def test_get_clicks_with_wrong_http_methods(client):
    create_url_response = client.post('/lil/shorten-url', json={'url': 'https://github.com'})
    new_url = create_url_response.get_json().get('short_url', None)

    post_response = client.post(new_url + '/clicks')
    put_response = client.put(new_url + '/clicks')
    patch_response = client.patch(new_url + '/clicks')

    assert post_response.status_code == 405
    assert put_response.status_code == 405
    assert patch_response.status_code == 405


def test_get_all(client):
    get_all_response = client.get('/lil/get-all')
    get_all_response_data = get_all_response.get_json()

    assert get_all_response.status_code == 200
    assert get_all_response_data is not None
    assert type(get_all_response_data) == list
    assert type(get_all_response_data[0]) == dict
    assert len(get_all_response_data) > 0


def test_get_all_with_wrong_http_methods(client):
    post_response = client.post('/lil/get-all')
    put_response = client.put('/lil/get-all')
    patch_response = client.patch('/lil/get-all')

    assert post_response.status_code == 405
    assert put_response.status_code == 405
    assert patch_response.status_code == 405
