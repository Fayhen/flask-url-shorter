import config
from hashids import Hashids


hashmaker = Hashids(min_length=4, salt=config.SECRET_KEY)


def hash_url(url):
    print(url)
    a_number = 3
    hash_id = hashmaker.encode(a_number)

    return hash_id
