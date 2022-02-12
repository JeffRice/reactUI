import logging
from uuid import uuid4
from datetime import datetime
from flask import Flask, jsonify, request, abort
from server.calculation import Calculation
from server.calculation_machine import CalculationMachine

def create_app(machine: CalculationMachine, auth: bool = True):

    app = Flask(__name__)
    user_token = None
    user_calc_ids = set()
    
    def set_user_token(uuid):
        user_token = uuid

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
        if not (params.get('username') and params.get('password')):
            return log_and_return("Posted json must contain a `username` and `password`", 400)
        if params['password'] != 'password':
            return log_and_return("Invalid credentials", 401)
        set_user_token(uuid4())
        return { "token": user_token }

    @app.route('/calculations', methods=['GET'])
    def list():
        return jsonify([calc.summary(time=datetime.now()) for calc in machine.values()])

    @app.route('/calculations/<uuid>', methods=['GET'])
    def get_detail(uuid):
        if uuid not in machine:
            return log_and_return("Unknown Calculation ID", 404)
        return machine[uuid].detail(time=datetime.now())

    @app.route('/calculations', methods=['POST'])
    def start():
        params = request.get_json()
        if params.id:
            return log_and_return("You cannot provide an ID for a new calculation", 400)
        calc = Calculation.create(
            user_id=user_token_header(),
            inputs=py_.pick(params, 'foo', 'bar', 'baz', 'calc_type')
        )
        calculations.add(calc)
        return {
            id: calc.id
        }

    @app.route('/calculation/<uuid>/cancel', methods=['PATCH'])
    def cancel(uuid):

        if not is_user_calc_id(uuid):
            return log_and_return("Unknown calculation ID, or ID does not belong to this user.", 400)

        machine.cancel(uuid)
        return 200

    return app
