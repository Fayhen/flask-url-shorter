from api.models import Url


def test_create_new_url(db):
    new_url = Url.create_new(long_url="https://github.com")

    assert new_url.id
    assert new_url.long_url
    assert new_url.hash
    assert type(new_url.clicks) == int
    assert new_url.clicks >= 0


def test_get_url_by_hash(db):
    new_url = Url.create_new(long_url="https://github.com")

    queried_hash = Url.get_url_by_hash(new_url.hash)

    assert queried_hash is not None
    assert queried_hash.id == new_url.id


def test_instance_serialization(db):
    new_url = Url.create_new(long_url="https://github.com")

    serialized_url = new_url.serialize()

    assert 'clicks' in serialized_url
    assert 'long_url' in serialized_url
    assert 'hash' in serialized_url

    assert serialized_url['clicks'] == new_url.clicks
    assert serialized_url['long_url'] == new_url.long_url
    assert serialized_url['hash'] == new_url.hash


def test_url_list_serialization(db):
    for i in range(5):
        Url.create_new(long_url="https://github.com")

    urls = Url.query.all()
    serialized_urls = Url.serialize_list(urls)

    assert urls is not None
    assert type(serialized_urls) == list
    assert type(serialized_urls[0]) == dict
    assert len(serialized_urls) == len(urls)
