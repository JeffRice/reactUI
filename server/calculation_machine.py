import logging
import time
import random
from threading import Thread
from typing import List, Optional
from datetime import datetime
from collections.abc import Mapping
from pydash import py_
from server.calculation import Calculation, random_true


def loop_in_thread(f, calc_delay):
    def loop():
        while True:
            f()
            time.sleep(calc_delay())
    Thread(target=loop).start()


class CalculationMachine(Mapping):

    def __init__(self):
        self.calculations = {}
        self.other_user_calc_ids = []

    def __getitem__(self, uuid):
        return self.calculatons[uuid]

    def __iter__(self):
        return iter(self.calculations)

    def __len__(self):
        return len(self.calculations)

    def add(self, c):
        logging.info(f"Adding calc {c}")
        self.calculations[c.id] = c

    def cancel(self, uuid):
        logging.info(f"Cancelling {uuid}")
        self.calculations[uuid] = self.calculations[uuid].cancelled(datetime.now())

    def error(self, uuid, error):
        logging.info(f"Error: {uuid}, {error}")
        self.calculations[uuid] = self.calculations[uuid].errored(error, datetime.now())

    def simulate_other_users(self):
        def f():
            calc = Calculation.random()
            self.add(calc)
            self.other_user_calc_ids.append(calc.id)
        loop_in_thread(f, lambda: random.randint(5, 60))

    def simulate_cancellations(self):
        def f():
            # cancel a calc every once in a while
            if self.other_user_calc_ids:
                victim = random.choice(self.other_user_calc_ids)
                self.cancel(victim)
        loop_in_thread(f, lambda: random.randint(30, 120))

    def simulate_errors(self):

        errors = [
            "Lost connection to sensor",
            "Radiation interference",
            "Capacitor failed to flux"
        ]

        def f():
            sleep = random.randint(5, 120)
            time.sleep(sleep)
            if self.calculations:
                victim = random.choice(list(self.calculations.keys()))
                error = random.choice(errors)
                self.error(victim, error, datetime.now())
        loop_in_thread(f, random.randint(10, 60))
