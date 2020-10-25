from .fixtures import test_api_client
from json import loads
from os import listdir
from os.path import isdir
from pytest import mark
from .fixtures import config, get_logger
from .fixtures import AppConfig, get_file_contents
from .fixtures import make_file_name, write_json


def test_app_config():
    assert AppConfig().retrieve_environment() == config
    assert len([{k: v} for k, v in config.items() if len(v) < 1]) == 0
    assert config['env'] in ('DEV', 'UAT', 'PROD')
    assert isdir(config['file_store'])


def test_uuid():
    assert len(make_file_name()) > 0


def test_write_file_store():
    file_name = 'pytest_test_json_file.txt'
    write_json(file_name, {'PYTEST': 'testing'})
    assert 'PYTEST' in get_file_contents(file_name)


@mark.xfail()
def test_get_file_store_error(test_api_client):
    response = test_api_client.get('/api/v1/get_file_store',
                                   headers={'FileName': 'zzz123'},
                                   follow_redirects=True)

    assert response.status_code == 400
    assert 'Error' in loads(response.get_data())


def test_post_get_file_store(test_api_client):
    response = test_api_client.post('/api/v1/post_file_store',
                                    json={'FileData': {'PYTEST': 'test data'}},
                                    follow_redirects=True,
                                    content_type='application/json')

    assert response.status_code == 200
    resp = loads(response.get_data())
    assert 'Created' in resp
    assert resp['Created']
    assert 'FileName' in resp
    assert len(resp['FileName']) > 0

    file_name = resp['FileName']
    response = test_api_client.get('/api/v1/get_file_store',
                                   headers={'FileName': file_name},
                                   follow_redirects=True)

    assert response.status_code == 200
    resp = loads(response.get_data())
    assert file_name in resp
    assert 'PYTEST' in resp[file_name]
    assert resp[file_name]['PYTEST'] == 'test data'


@mark.xfail()
def test_post_file_store_error(test_api_client):
    initial = listdir(config['file_store'])
    response = test_api_client.post('/api/v1/post_file_store',
                                    # Use bad JSON key (should be FileData)
                                    json={'FileName': {'PYTEST': 'test data'}},
                                    follow_redirects=True,
                                    content_type='application/json')
    updated = listdir(config['file_store'])
    assert response.status_code == 400
    resp = loads(response.get_data())
    assert 'Created' in resp
    assert resp['Created'] is False
    assert initial == updated


def test_logger():
    assert get_logger(__name__) is not None
