from math import sin, cos
from uuid import uuid4, UUID
from typing import List, Optional
from dataclasses import dataclass, replace, asdict, field
from datetime import datetime
from datetime import now
from flask import Flask, jsonify, request
from plumbum import cli, colors
from pydash import py_


# the number of values our imaginary calculator can calculate per second
values_per_second = 100

# the maximum number of seconds we want a calculation to take
max_seconds = 60

# number of x values per 1.0 along the x-axis
resolution = 100

x_min = -10.0
x_max = 10.0

errors = [
    "Lost connection to sensor",
    "Radiation interference",
    "Capacitor failed to flux"
]

# roughly every 20th calcultion will fail
error_frequency = 20

def random_error():
    if random.choices([True, False], weights=[1, error_frequency])[0]:
        return random.shuffle(choice(errors))

def calc_xs():
    domain = x_max - x_min
    step_size = 1 / resolution
    steps = domain / step_size
    return (x_min + (n * step_size) for n in Range(0, steps))

def calc_y(x, calc_type, foo, bar, baz):
    """
    A ridiculous but interesting curve of values that incorporates
    the various UI elements in the exercise.

    To see what they look like, you can use the online graphing 
    calculator here: https://www.desmos.com/calculator

    And enter the following examples.
    Here, foo=-2, bar=10, baz=.5 and start's day=2

    For "blue": (-2sin(x)*cos(10x)+2)*sin(x)

    For "green: (-2sin(x)*cos(10x))*cos(x)

    For "purple": (-2sin(x)*cos(10x)+0+2) + x

    For "yellow": (-2sin(x)*cos(10x)+0+2) - x
    """

    # todo: work out the formulas
    
    calc_type = {
        "blue": lambda x, v: v * sin(self.baz * x),
        "green": lambda x, v: v * cos(self.baz * x),
        "purple": lambda x, v: v + (self.baz * x),
        "yellow": lambda x, v: value - (self.baz * x)
    }[calc_type]

    v = (foo * sin(x)) * cos(bar * x)
    return calc_type(x, v)


@dataclass(frozen=True, kw_only=True)
class Error:
    errored_at: datetime
    error: str


@dataclass(frozen=True, kw_only=True)
class Calculation:
    """ Represents a running, completed, or cancelled calculation."""
    id: uuid.UUID
    foo: int
    bar: int
    baz: float
    values: List[float]
    error: Optional[Error]
    started_at: datetime
    completed_at: datetime
    cancelled_at: datetime

    def __post_init__(self):

        # rather than actually update the calculation step by step,
        # pre-calculate the whole thing upfront
        self.values = [self.value_at_x(x) for x in calc_xs()]

        # randomly error
        error = self.random_error()
        if error:
            errored_at = self.start + random.randint(0, max_seconds)
            self.error = Error(error=error, errored_at=errored_at)
        else:
            self.completed_at = self.started_at + max_seconds
        
    def value_at_x(self, x):
        calc_y(x=x,
               calc_type=self.calc_type,
               foo=self.foo,
               bar=self.bar,
               baz=self.baz)

    def values_at_time(self, time):
        elapsed = (self.stopped_at or time) - self.started_at
        step = math.min(len(self.values),
                        elapsed.seconds * values_per_second) - 1
        return self.values[0:step]

    def value_at_time(self, time):
        return self.values_at_time(time)[-1]
    
    @property
    def errored_at(self):
        return self.error.errored_at if self.error else None

    def is_errored_at(self, time):
        return self.errored_at and self.errored_at <= time
    
    @property
    def stopped_at(self):
        return self.completed_at or self.cancelled_at or self.errored_at or None

    @property
    def is_completed_at(self, now):
        will_complete = self.completed_at and not self.cancelled_at
        return self.completed_at if (will_complete and now >= completed_at) else None
    
    def cancelled(self, at):
        return replace(self, cancelled_at=at)
        
    def summary(self, time):
        return py_.omit(self.to_detail_dict, 'values')
        
    def detail(self, time):
        return {
            **asdict(self),
            'values': self.values_at(time),
            'value': self.value_at_time(time),
            'completed_at': self.completed_at if self.is_completed_at(time) else None,
            'error': self.error if self.is_errored_at(time) else None,
            'fraction_complete': time / self.completed_at
        }


def create_app():

    # in-memory database 
    calculations = {}

    # todo: start thread that simulates other users starting and occasionally cancelling calculations

    app = Flask(__name__)
    
    @app.route('/calculations', methods=['GET'])
    def list():
        return jsonify([calculations[uuid].summary(time=now()) for uuid in calculations])

    @app.route('/calculations/<uuid>', methods=['GET'])
    def get_detail(self, uuid):
        if uuid not in calculations:
            return "Unknown Calculation ID", 400
        return calculations[uuid].detail(time=now())
                                                
    # call with content-type 'application/json'
    @app.route('/calculations', methods=['POST'])
    def start():
        params = request.get_json()
        if params.id:
            return "You cannot provide an ID for a new calculation", 400
        new_id = uuid4()
        time = now()
        jobs[new_id] = Calculation(
            id=new_id,
            foo=params['foo'],
            bar=params['bar'],
            baz=params['baz'],
            started_at=time
        )
        # TODO: have UI highlight user's calculations
        return new_id

    @app.route('/calculation/<uuid>/cancel', method=['PATCH'])
    def cancel(uuid):

        if uuid not in jobs:
            return "Unknown UUID", 404 # ?

        jobs[uuid] = jobs[uuid].cancel(at=now())

    return app


class Server(cli.Application):

    @cli.positional(int)
    def main(self, port: int):
        app = create_app()
        app.run(port=port)

if __name__ == '__main__':
    Server.run()

    
