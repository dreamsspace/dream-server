import tempfile

import pytest

from server import app
from server.db import dream as dream_mod
from server.schema.dream import dream_survey_schema


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def dream_db_mock():
    with tempfile.TemporaryDirectory() as tmpdir:
        new_dream_db = dream_mod.DreamDB(tmpdir)
        dream_mod.dream_db = new_dream_db
        yield


def test_healthcheck(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_login(client):
    resp = client.post(
        '/login', json={'username': 'joe', 'password': 'baseball'},
    )
    assert resp.status_code == 200
    assert resp.json['user_id']


def test_add_dream(client):
    resp = client.post(
        '/dream', json={'user_id': '123', 'contents': 'dream content'},
    )
    assert resp.status_code == 200
    assert resp.is_json

    # Response should succesfully deserialize to DreamSurvey
    assert dream_survey_schema.load(resp.json)


def test_get_dreams(client):
    resp = client.post(
        '/login', json={'username': 'joe', 'password': 'baseball'},
    )
    assert resp.status_code == 200
    user_id = resp.json['user_id']
    
    resp = client.post(
        '/dream', json={'user_id': user_id, 'contents': 'foobar'},
    )
    assert resp.status_code == 200

    resp = client.get(f'/dream-log?user_id={user_id}')
    assert resp.status_code == 200
    # assert resp.json
