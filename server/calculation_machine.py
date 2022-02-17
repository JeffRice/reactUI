import logging
import time
import random
import math
from threading import Thread
from typing import List, Optional
from datetime import datetime
from collections.abc import Mapping
from pydash import py_
from server.calculation import Calculation


def loop_in_thread(f, calc_delay):
    def loop():
        while True:
            time.sleep(calc_delay())
            f()
    Thread(target=loop).start()

def variable_delay(frequency):
    min_freq = max(0, math.ceil(frequency * .50))
    max_freq = math.ceil(frequency * 1.50)
    return lambda: random.randint(min_freq, max_freq)
    

class CalculationMachine(Mapping):

    def __init__(self):
        self.calculations = {}
        self.other_user_calc_ids = []

    def __getitem__(self, uuid):
        return self.calculations[uuid]

    def __iter__(self):
        return iter(self.calculations)

    def __len__(self):
        return len(self.calculations)

    def add(self, c):
        logging.info(f"Adding calc {c.id}")
        self.calculations[c.id] = c

    def cancel(self, uuid):
        logging.info(f"Cancelling {uuid}")
        self.calculations[uuid] = self.calculations[uuid].cancelled(datetime.now())

    def error(self, uuid, error):
        logging.info(f"Error: {uuid}, {error}")
        self.calculations[uuid] = self.calculations[uuid].errored(error, datetime.now())

    def simulate_other_users(self, frequency):
        def f():
            calc = Calculation.random()
            self.add(calc)
            self.other_user_calc_ids.append(calc.id)
        loop_in_thread(f, variable_delay(frequency))

    def simulate_cancellations(self, frequency):
        def f():
            # cancel a calc every once in a while
            if self.other_user_calc_ids:
                victim = random.choice(self.other_user_calc_ids)
                self.cancel(victim)
        loop_in_thread(f, variable_delay(frequency))

    def simulate_errors(self, frequency):

        errors = [
            "Lost connection to sensor",
            "Radiation interference",
            "Capacitor failed to flux"
        ]

        def f():
            if self.calculations:
                victim = random.choice(list(self.calculations.keys()))
                error = random.choice(errors)
                self.error(victim, error)
        loop_in_thread(f, variable_delay(frequency))

    def start_expiration_thread(self, retain_for):
        def f():
            now = datetime.now()
            def is_expired(calc):
                stopped_at = calc.stopped_at(now)
                elapsed = stopped_at and (now - stopped_at).seconds or 0
                return elapsed >= retain_for
            expired = [uuid for uuid, calc in self.items() if is_expired(calc)]
            for uuid in expired:
                logging.info(f"Forgetting {self.calculations[uuid]}")
            self.calculations = py_.omit(self.calculations, *expired)
            self.other_user_calc_ids = [uuid for uuid in self.other_user_calc_ids if uuid in self.calculations]
        loop_in_thread(f, lambda: 1)
