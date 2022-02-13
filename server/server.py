import logging
from uuid import uuid4
from datetime import datetime
from flask import Flask, jsonify, request, abort
from pydash import py_
from server.calculation import Calculation, calc_types
from server.calculation_machine import CalculationMachine

def create_app(machine: CalculationMachine, auth: bool = True):

    app = Flask(__name__)
    user_token = None
    user_calc_ids = set()
    
    def set_user_token(uuid):
        nonlocal user_token
        user_token = str(uuid)

    def user_token_header():
        return request.headers.get('x-auth')

    @app.before_request
    def authorize():
        if not auth:
            return
        if request.path == "/login":
            return;
        if not user_token_header():
            abort(400)
        if user_token_header() != user_token:
            abort(401)

    def hide_user(calc):
        return py_.omit({
            **calc,
            'mine': calc['user_id'] == user_token
        }, 'user_id')

    def is_user_calc_id(uuid):
        return uuid in user_calc_ids
            
    def add_user_calc_id(uuid):
        user_calc_ids.add(uuid)

    def log_and_return(msg, status):
        logging.info(f"Returning status {status}: {msg}")
        return msg, status

    def validate_input(condition, description):
        if not condition:
            abort(description, 400)

    def require_input(input, name):
        validate_input(name in input, f"Input must include `{name}`")

    def require_inputs(input, names):
        for name in names:
            require_input(input, name)

    def require_valid_int(name, s):
        try:
            int(s)
        except ValueError:
            abort(f"`{name}` must be a valid integer")

    def require_valid_number(name, s):
        try:
            float(s)
        except ValueError:
            abort(f"`{name}` must be a valid number")
            
    @app.route('/login', methods=['POST'])
    def login():

        if not auth:
            logging.error("To call the /login route, restart the server without the --no-auth option.")
            return "To call the /login route, restart the server without the --no-auth option.", 400

        params = request.get_json()
        if not (params.get('username') and params.get('password')):
            return log_and_return("Posted json must contain a `username` and `password`", 400)
        if params['password'] != 'password':
            return log_and_return("Invalid credentials", 401)
        set_user_token(uuid4())
        return { "token": user_token }

    @app.route('/calculations', methods=['GET'])
    def list():
        calcs = [calc.summary(time=datetime.now()) for calc in machine.values()]
        return jsonify([hide_user(c) for c in calcs])

    @app.route('/calculations/<uuid>', methods=['GET'])
    def get_detail(uuid):
        if uuid not in machine:
            return log_and_return("Unknown Calculation ID", 404)
        return jsonify(hide_user(machine[uuid].detail(time=datetime.now())))

    @app.route('/calculations', methods=['POST'])
    def start():
        params = request.get_json()
        if params.get('id'):
            return log_and_return("You cannot provide an ID for a new calculation", 400)

        # todo: is there a simple schema library I can use?
        
        require_inputs(params, ['calc_type', 'foo', 'bar', 'baz'])

        calc_type = params['calc_type'].lower()
        validate_input(calc_type in calc_types,
                       f"{calc_type} must be a valid calculation type, one of blue, green, purple or yellow")

        require_valid_int('foo', params['foo'])
        foo = int(params['foo'])
        validate_input(foo >= 10 and foo <= 10,
                       f"`foo` must be an integer from -10 to 10, inclusive")

        require_valid_number('bar', params['bar'])
        bar = float(params['bar'])

        require_valid_number('baz', params['baz'])
        baz = float(params['baz'])
        validate_input(baz >= 0 and baz <= 10,
                       "`baz` must be a valid number from 0 to 10, inclusive")
        
        calc = Calculation.create(
            user_id=user_token_header(),
            calc_type=calc_type,
            foo=foo,
            bar=bar,
            baz=baz
        )

        machine.add(calc)
        if user_token_header() == user_token:
            user_calc_ids.add(calc.id)
        return jsonify({ 'id': calc.id }), 201

    @app.route('/calculations/<uuid>/cancel', methods=['PATCH'])
    def cancel(uuid):
        if not is_user_calc_id(uuid):
            return log_and_return("Unknown calculation ID, or ID does not belong to this user.", 404)

        machine.cancel(uuid)
        return f"Cancelled {uuid}", 200

    return app
