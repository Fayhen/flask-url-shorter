from api.validators import validate_url


def test_validate_url():
    valid_url = 'https://www.example.com'
    valid_url_with_http = 'http://www.example.com'
    valid_url_with_geo_domain = 'https://www.example.com.br'
    valid_url_with_trailing_slash = 'https://www.example.com/'
    valid_url_with_path = 'https://www.example.com/path'
    valid_url_with_paths = 'https://www.example.com/path/resource'
    valid_url_with_query_parameters = 'https://www.example.com/view?page=3&amount=25'
    valid_url_without_www = 'https://example.com'

    invalid_url_no_protocol = 'www.example.com'
    invalid_url_typo_protocol = 'httsp://www.example.com'
    invalid_url_no_format = 'not_a_url'

    assert validate_url(valid_url)
    assert validate_url(valid_url_with_http)
    assert validate_url(valid_url_with_geo_domain)
    assert validate_url(valid_url_with_trailing_slash)
    assert validate_url(valid_url_with_path)
    assert validate_url(valid_url_with_paths)
    assert validate_url(valid_url_with_query_parameters)
    assert validate_url(valid_url_without_www)

    assert not validate_url(invalid_url_no_protocol)
    assert not validate_url(invalid_url_typo_protocol)
    assert not validate_url(invalid_url_no_format)
