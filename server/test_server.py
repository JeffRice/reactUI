import json
import pytest
import time
from pydash import py_
from uuid import uuid4
from contextlib import contextmanager
from server.server import create_app
from server.calculation_machine import CalculationMachine

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
    machine = CalculationMachine()
    app = create_app(machine=machine, auth=auth)
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
def client_with_login(client_no_login):
    response = _login(client_no_login, data=correct_login)
    assert response.status_code == 200
    token = response.get_json()['token']
    yield ClientWithHeaders(client_no_login, headers={'x-auth': token})

correct_login = { "username": "fred", "password": "password" }
        
def _login(client, data):
    return client.post("/login", data=json.dumps(data), content_type='application/json')
        
def _get_list(client):
    return client.get("/calculations")

def _get_detail(client, uuid):
    return client.get(f"/calculations/{uuid}")

def _create(client, data):
    return client.post("/calculations", data=json.dumps(data), content_type='application/json')

def _cancel(client, uuid):
    return client.patch(f"/calculations/{uuid}")


class TestLogin:

    def test_login_requires_auth_mode(self, client_no_auth):
        assert _login(client_no_auth, data=correct_login).status_code == 400
    
    def test_login_requires_valid_input(self, client_no_login):
        assert _login(client_no_login, data={}).status_code == 400
        assert _login(client_no_login, data={ "username": "h" }).status_code == 400
        assert _login(client_no_login, data={ "password": "password" }).status_code == 400

    def test_login_rejects_if_no_auth(self, client_no_auth):
        assert _login(client_no_auth, correct_login).status_code == 400

    def test_login_rejects_invalid_password(self, client_no_login):
        assert _login(client_no_login, data={ "username": "fred", "password": "hello" }).status_code == 401

    def test_login_returns_token(self, client_no_login):
        response = _login(client_no_login, data=correct_login)
        assert response.status_code == 200
        assert bool(response.get_json()['token'])

        
class TestAuth:
        
    def test_authorizes(self, client_no_login):
        assert _get_list(client_no_login).status_code == 401

    def test_no_auth_mode(self, client_no_auth):
        assert _get_list(client_no_auth).status_code == 200


class TestOperations:
    
    def test_operations(self, client_with_login):
        calc = {
            'calc_type': 'Blue',
            'foo': -3,
            'bar': 12,
            'baz': 4
        }

        create_response = _create(client_with_login, calc)
        assert create_response.status_code == 201
        created = create_response.get_json()
        calc_id = created['id']
        assert bool(calc_id)

        calcs = _get_list(client_with_login).get_json()
        assert len(calcs) == 1
        assert py_.pick(calcs[0], 'calc_type', 'foo', 'bar', 'baz', 'started_at') == calc
        assert calcs[0] == calc_id
        assert calcs[0]['mine']
        assert not bool(calcs[0]['error'])
        assert not bool(calcs[0]['cancelled_at'])
        assert not bool(calcs[0]['completed_at'])

        time.sleep(1)
        detail = _get_detail(client_with_login, calc_id).get_json()
        assert py_.pick(calcs[0], 'calc_type', 'foo', 'bar', 'baz', 'started_at') == calc
        assert detail['id'] == calc_id
        assert detail['mine']
        values = detail['values']
        assert values and len(values) < 500

        cancellation = _cancel(client_with_login, calc_id)
        assert cancellation.status_code == 200

        list_after_cancel = _get_list(client_with_login, calc_id).get_json()
        assert bool(list_after_cancel[0]['cancelled_at'])
        assert not list_after_cancel[0]['completed_at']

        detail_after_cancel = _get_detail(client_with_login, calc_id).get_json()
        assert bool(detail_after_cancel['cancelled_at'])
        assert not detail_after_cancel['completed_at']
        assert len(detail_after_cancel['values']) < 500

    def test_cancel_is_idempotent(self, client_with_login):

        calc = {
            'calc_type': 'Blue',
            'foo': -3,
            'bar': 12,
            'baz': 4
        }

        created = _create(client_with_login, calc).get_json()
        calc_id = created['id']

        assert _cancel(client_with_login, calc_id).status_code == 200
        assert _cancel(client_with_login, calc_id).status_code == 200


def _test_input_validation(client, name, invalid_value):
    valid_calc = { 'calc_type': 'blue', 'foo': -3, 'bar': 1, 'baz': 4 }

    missing_name = py_.omit(valid_calc, name)
    assert _create(client, missing_name) == 400

    with_invalid_value = { **valid_calc, name : invalid_value }
    assert _create(client, with_invalid_value) == 400
        
        
class TestInputValidation:
    
    def test_calc_type(self, client_no_auth):
        _test_input_validation(client_no_auth, name='calc_type', invalid_value='mango')
    
    def test_foo(self, client_no_auth):
        _test_input_validation(client_no_auth, name='foo', invalid_value='horse')
        _test_input_validation(client_no_auth, name='foo', invalid_value=-13)

    def test_bar(self, client_no_auth):
        _test_input_validation(client_no_auth, name='bar', invalid_value='otter')
    
    def test_baz(self, client_no_auth):
        _test_input_validation(client_no_auth, name='baz', invalid_value='whale')
        _test_input_validation(client_no_auth, name='baz', invalid_value=12)
    
    def test_cancel_invalid_uuid(self, client_no_auth):
        _create(client_no_auth, { 'calc_type': 'blue', 'foo': -3, 'bar': 1, 'baz': 4 })
        assert _cancel(client_no_auth, uuid4()) == 404

    def test_detail_invalid_uuid(self, client_no_auth):
        _create(client_no_auth, { 'calc_type': 'blue', 'foo': -3, 'bar': 1, 'baz': 4 })
        assert _get_detail(client_no_auth, uuid4()) == 404
    
