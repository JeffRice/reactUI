import pytest
from contextlib import contextmanager
from server.server import create_app


@contextmanager
def client(auth: bool):
    app = create_app(auth=auth)
    with app.test_client() as client:
        yield client
    
@pytest.fixture
def client():
    with client(auth=True) as c:
        yield c

@pytest.fixture
def client_no_auth():
    with client(auth=False) as c:
        yield c
    
@pytest.fixture
def client_with_login():
    with client_auth() as c:
        response = c.post("/login", data={
            "username": "fred",
            "password": "password"
        })
        token = response['token']
        yield ClientWithHeaders(headers={'x-auth': token})


class ClientWithHeaders:
    def __init__(self, client, headers):
        self.client = client
        self.headers = headers

    def get(self, route):
        return self.client(route, headers=self.headers)

    def post(self, route, data):
        return self.client(route, headers=self.headers, data=data)


def test_login_requires_valid_input(client):
    pass

def test_login_rejects_if_no_auth(client_no_auth):
    pass

def test_login_rejects_invalid_password():
    pass

def test_login_returns_token():
    pass

def test_list_authorizes():
    pass

def test_list_no_auth():
    pass

def test_list():
    pass

def test_create_calc_authorizes():
    pass

def test_create_calc_no_auth():
    pass

def test_create_calc():
    pass

def test_calc_detail_authorizes():
    pass

def test_calc_detail_no_auth():
    pass

def test_calc_detail():
    pass

def test_cancel_calc_authorizes():
    pass

def test_calcel_calc_no_auth():
    pass

def test_cancel_calc():
    pass


