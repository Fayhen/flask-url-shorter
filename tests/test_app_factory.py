from api import create_app


def test_config():
    """
    Tests whether passed configuration objects are added to the
    app, and if default configuration is in place if no such
    object is passed.
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
