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
