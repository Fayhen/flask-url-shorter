from api.models import Url
from api.methods import generate_hash, get_url_by_hash


def test_generate_hash():
    generated_hash = generate_hash(1)

    assert generated_hash is not None
    assert type(generated_hash) is str
    assert len(generated_hash) >= 4


def test_hash_uniqueness():
    integers = [*range(1000)]
    hash_list = [generate_hash(i) for i in integers]
    hash_set = set(hash_list)

    assert len(hash_set) == len(hash_list)


def test_get_url_by_hash(db):
    new_url = Url(long_url="https://github.com")
    db.session.add(new_url)
    db.session.commit()

    generated_hash = generate_hash(new_url.id)
    new_url.hash = generated_hash
    db.session.add(new_url)
    db.session.commit()

    print(new_url.serialize())

    queried_instance = get_url_by_hash(generated_hash)
    print(queried_instance.serialize())

    assert queried_instance is not None
    assert queried_instance.id == new_url.id
