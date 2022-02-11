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

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s")

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

    other_user_freq = cli.SwitchAttr("--other-user-freq",
                                     argtype=int,
                                     default=5,
                                     help="How often simulated users should start calculations, -1 for never.")

    other_user_cancel_freq = cli.SwitchAttr("--other-user-cancel",
                                            argtype=int,
                                            default=10,
                                            help="How often simulated users should cancl their calculations. -1 for never.")

    error_freq = cli.SwitchAttr("--error-freq",
                                argtype=int,
                                default=30,
                                help="How often errors should occur. -1 for never")
    
    seed = cli.SwitchAttr("--seed",
                          argtype=int,
                          default=5,
                          help="Number of running calculations to seed the machine with.")

    @cli.positional(int)
    def main(self, port: int):

        machine = CalculationMachine()
        # app = create_app(machine)

        if self.error_freq != -1:
            logging.info(f"Simulating errors roughly every {self.error_freq} seconds")
            machine.simulate_errors(frequency=self.error_freq)

        if self.other_user_cancel_freq != -1:
            logging.info(f"Simulating other users cancelling calculations roughly every {self.other_user_cancel_freq} seconds.")
            machine.simulate_cancellations(frequency=self.other_user_cancel_freq)

        if self.other_user_freq != -1:
            logging.info(f"Simulating other users starting calculations roughly every {self.other_user_freq} seconds.")
            machine.simulate_other_users(frequency=self.other_user_freq)


        logging.info(f"Seeding machine with {self.seed} running calculations.")
        for _ in range(self.seed):
            machine.add(Calculation.random())

        # app.run(port=port)
        # logging.info(f"Server listening on port {port}")


if __name__ == '__main__':
    Server.run()
