import config
from hashids import Hashids
from api.models import Url


hashmaker = Hashids(min_length=4, salt=config.SECRET_KEY)


def generate_hash(url_id):
    """
    Generates a new short hash using an URL's ID, making it unique.
    """
    new_hash = hashmaker.encode(url_id)

    return new_hash


def get_url_by_hash(hashed_id):
    """
    Returns the full URL corresponding to the hash passed as argument.
    """
    url_instance = Url.query.filter_by(hash=hashed_id).first()

    return url_instance if url_instance else None
