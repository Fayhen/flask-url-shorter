import config
from hashids import Hashids
from api.models import Url


hashmaker = Hashids(min_length=4, salt=config.SECRET_KEY)


def get_last_url_id():
    """
    Queries the last URL added to the database and returns its ID.
    """
    last_url = Url.query.order_by(Url.id.desc()).first()

    return last_url.id


def generate_hash():
    """
    Generates a new short hash using the next URL ID to be added to
    the database.
    """
    last_id = get_last_url_id()
    new_hash = hashmaker.encode(last_id + 1)

    return new_hash


def generate_hash_with_id(id):
    """
    Generates a new short hash using an URL's ID, making it unique.
    """
    new_hash = hashmaker.encode(id)

    return new_hash


def get_full_url(hashed_id):
    """
    Returns the full URL corresponding to the hash passed as argument.
    """
    url_instance = Url.query.filter_by(hash=hashed_id).first()

    if url_instance:
        return url_instance.long_url

    return None
