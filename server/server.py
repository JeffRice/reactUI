import logging
import time
import random
from typing import List, Optional
from datetime import datetime
from flask import Flask, jsonify, request
from plumbum import cli, colors
from pydash import py_
from server.calculation import Calculation, random_true
from server.calculation_machine import CalculationMachine

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

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

class Server(cli.Application):

    simulate_other_users = cli.Flag("--no-other-users",
                                    default=True,
                                    help="Will not simulate other users creating and cancelling calculations")

    simulate_errors = cli.Flag("--no-errors",
                               default=True,
                               help="Will not simulate calculations encountering errors")

    simulate_cancellations = cli.Flag("--no-cancels",
                                      default=True,
                                      requires=['--no-other-users'],
                                      help="Will not simulate other users cancelling their calculations")

    seed = cli.SwitchAttr("--seed",
                          argtype=int,
                          default=5,
                          help="Number of running calculations to seed the machine with.")

    @cli.positional(int)
    def main(self, port: int):

        machine = CalculationMachine()

        for _ in range(self.seed):
            machine.add(Calculation.random())

#        app = create_app(machine)

#        app.run(port=port)
#        logging.info(f"Server listening on port {port}")

        if self.simulate_errors:
            logging.info("Simulating errors.")
            machine.simulate_errors()

        if self.simulate_other_users:
            logging.info("Simulating other users.")
            machine.simulate_other_users()

        if self.simulate_cancellations:
            logging.info("Simulating other users cancelling calculations.")
            machine.simulate_cancellations()


if __name__ == '__main__':
    Server.run()
