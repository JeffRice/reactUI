import logging
from uuid import uuid4
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from pydash import py_
from server.calculation import Calculation, calc_types
from server.calculation_machine import CalculationMachine

from marshmallow import Schema, fields


class LoginInputSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    
class CreateCalcInputSchema(Schema):
    calc_type = fields.Str(required=True, validate=lambda s: s.lower() in calc_types)
    foo = fields.Int(required=True, validate=lambda n: -10 <= n and n <= 10)
    bar = fields.Float(required=True)
    baz = fields.Float(required=True, validate=lambda n: 0 <= n and n <= 10)


def create_app(machine: CalculationMachine, auth: bool = True):

    app = Flask(__name__)

    # allow from all domains
    CORS(app)
    
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
            
    @app.route('/login', methods=['POST'])
    def login():

        if not auth:
            logging.error("To call the /login route, restart the server without the --no-auth option.")
            return "To call the /login route, restart the server without the --no-auth option.", 400

        params = request.get_json()

        errors = LoginInputSchema().validate(params)
        if errors:
            abort(400, str(errors))

        if params['password'] != 'password':
            return log_and_return("Invalid credentials", 401)

        set_user_token(uuid4())

        return { "token": user_token }

    @app.route('/calculations', methods=['GET'])
    def get_list():
        calcs = [calc.summary(time=datetime.now()) for calc in list(machine.values())]
        return jsonify([hide_user(c) for c in calcs])

    @app.route('/calculations/<uuid>', methods=['GET'])
    def get_detail(uuid):

        seconds_str = request.args.get("at")
        if seconds_str and not is_valid_int(seconds_str):
            abort(400, "at must be an integer")

        if uuid not in machine:
            return log_and_return("Unknown Calculation ID", 404)

        calc = machine[uuid]
        time = calc.started_at + timedelta(seconds=int(seconds_str)) if seconds_str else datetime.now()

        return jsonify(hide_user(machine[uuid].detail(time=time)))

    @app.route('/calculations', methods=['POST'])
    def start():
        params = request.get_json()

        errors = CreateCalcInputSchema().validate(params)
        if errors:
            abort(400, str(errors))
        
        calc = Calculation.create(
            user_id=user_token_header(),
            inputs = {
                'calc_type': params['calc_type'].lower(),
                'foo': int(params['foo']),
                'bar': float(params['bar']),
                'baz': float(params['baz'])
            })

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

def is_valid_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
