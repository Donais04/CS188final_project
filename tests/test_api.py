from urllib import response

from final_project.app import create_app
from final_project.db import changeDB
import pytest

@pytest.fixture
def client(tmp_path):
    app = create_app(dbName=tmp_path / "testing.db")
    changeDB(tmp_path / "testing.db")
    app.testing = True
    with app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Hello, World!'}

def test_register(client):
    response = client.post('/register', json={'username': 'testuser', 'password': 'testpass123', 'displayname': 'aaa'}) #test registering a new user
    assert response.status_code == 201
    assert response.json == {'message': 'User testuser registered successfully'}

    response = client.post('/register', json={'username': 'testuser', 'password': 'testpass123', 'displayname': 'aaa'}) #test registering a user that already exists
    assert response.status_code == 400
    assert response.json == {'message': 'User testuser already exists'}

    response = client.post('/register', json={'password': 'testpass123'}) #testing missing some
    assert response.status_code == 400
    assert response.json == {'message': 'User testuser already exists'}

    response = client.post('/register', json={'username': 'testuser', 'password': '1', 'displayname': 'aaa'}) #test bad password
    assert response.status_code == 400
    assert response.json == {'message': 'User testuser already exists'}

    response = client.post('/register', json={'username': 1, 'password': 'testpass123', 'displayname': 'aaa'}) #test wrong type
    assert response.status_code == 400
    assert response.json == {'message': 'User testuser already exists'}

    response = client.post('/register', json={'username': 1, 'password': 'testpass123', 'displayname': ['aaa','bbb']}) #test wrong type
    assert response.status_code == 400
    assert response.json == {'message': 'User testuser already exists'}