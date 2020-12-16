from .fixtures import test_api_client, config


def test_index(test_api_client):
    response = test_api_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'<title>%s</title>' % config['company'].encode() in response.get_data()


def test_index_redirect_no_follow(test_api_client):
    response = test_api_client.get('/non-existing-page', follow_redirects=False)
    assert response.status_code == 302


def test_index_redirect_follow(test_api_client):
    response = test_api_client.get('/non-existing-page', follow_redirects=True)
    assert response.status_code == 200
    assert b'<title>%s</title>' % config['company'].encode() in response.get_data()
