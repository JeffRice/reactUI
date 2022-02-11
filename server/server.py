import logging
from datetime import datetime
from flask import Flask, jsonify, request
from plumbum import cli, colors
from server.calculation import Calculation

def create_app(machine):

    app = Flask(__name__)

    @app.route('/calculations', methods=['GET'])
    def list():
        return jsonify([calc.summary(time=datetime.now()) for calc in machine.values()])

    @app.route('/calculations/<uuid>', methods=['GET'])
    def get_detail(self, uuid):
        if uuid not in machine:
            return "Unknown Calculation ID", 404
        return machine[uuid].detail(time=datetime.now())

    # call with content-type 'application/json'
    @app.route('/calculations', methods=['POST'])
    def start():
        params = request.get_json()
        if params.id:
            return "You cannot provide an ID for a new calculation", 400
        calc = Calculation(
            id=new_id,
            foo=params['foo'],
            bar=params['bar'],
            baz=params['baz'],
            started_at=datetime.now()
        )
        calculations.add(calc)
        return {
            id: calc.id
        }

    @app.route('/calculation/<uuid>/cancel', method=['PATCH'])
    def cancel(uuid):

        if uuid not in jobs:
            return "Unknown UUID", 404

        machine.cancel(uuid)

        return 200

