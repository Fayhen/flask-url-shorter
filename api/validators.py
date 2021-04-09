import re


def validate_url(url):
    pattern = re.compile(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/){1}[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
    valid = re.match(pattern, url)

    if bool(valid):
        return True

    return False
