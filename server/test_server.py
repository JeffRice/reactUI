import pytest
from contextlib import contextmanager
from server.server import create_app


class ClientWithHeaders:
    def __init__(self, client, headers):
        self.client = client
        self.headers = headers

    def get(self, *args, **kwargs):
        return self.client.get(*args, headers=self.headers, **kwargs)

    def post(self, *args, **kwargs):
        return self.client.post(*args, headers=self.headers, **kwargs)

    def patch(self, *args, **kwargs):
        return self.client.patch(*args, headers=self.headers, **kwargs)


@contextmanager
def _client(auth: bool):
    app = create_app(auth=auth)
    with app.test_client() as client:
        yield client

@pytest.fixture
def client_no_auth():
    with _client(auth=False) as c:
        yield c

@pytest.fixture
def client_no_login():
    with _client(auth=True) as c:
        yield c

@pytest.fixture
def client_with_login():
    with client_auth() as c:
        response = _login(c, data=correct_login)
        token = response['token']
        yield ClientWithHeaders(headers={'x-auth': token})

correct_login = { "username": "fred", "password": "password" }
        
def _login(client, data):
    return client.post("/login", data=data)
        
def _get_list(client):
    return client.get("/calculations")

def _get_detail(client, uuid):
    return client.get(f"/calculations/{uuid}")

def _create(client, data):
    return client.post("/calculations", data=data)

def _cancel(client, uuid):
    return client.patch(f"/calculations/{uuid}")


class TestLogin:

    def test_login_requires_auth_mode(client_no_auth):
        assert _login(client_no_auth, data=correct_login).status_code == 400
    
    def test_login_requires_valid_input(client_no_login):
        assert _login(client, data={}).status_code == 400
        assert _login(client, data={ "username": "h" }).status_code == 400
        assert _login(client, data={ "password": "password" }).status_code == 400

    def test_login_rejects_if_no_auth(client_no_auth):
        assert _login(client_no_auth, correct_login).status_code == 400

    def test_login_rejects_invalid_password(client_no_login):
        assert _login(client, data={ "username": "fred", "password": "hello" }).status_code == 401

    def test_login_returns_token(client_no_login):
        response = _login(client, data=correct_login)
        assert response.status_code == 200
        assert bool(response.get_json()['token'])

        
class TestAuth:
        
    def test_authorizes(client_no_login):
        assert _get_list(client_no_login).status_code == 401

    def test_no_auth_mode(client_no_auth):
        assert _get_list(client_no_auth).status_code == 200

    
def test_operations(client_with_login):
    pass

