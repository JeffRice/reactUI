import random
from math import sin, cos, ceil
from uuid import uuid4, UUID
from typing import List, Optional
from dataclasses import dataclass, replace, asdict, field
from datetime import datetime, timedelta
from pydash import py_

# the maximum number of seconds we want a calculation to take
max_seconds = 60

# number of x values per 1.0 along the x-axis
resolution = 100


@dataclass(frozen=True)
class Error:
    errored_at: datetime
    error: str

@dataclass(frozen=True)
class Calculation:
    """ Simulates a long-running calculation that updates a value
    over a period of time until it arrives at the final answer,
    like a differential equation.

    You give it the input values and the list of intermediate `values`,
    and `values_per_second` to dictate how quickly the calculation should
    simulate its progress, and at any given point it will provide
    its simulated state.
    """
    id: UUID

    calc_type: str
    started_at: datetime

    # any integer from -10 to +10, inclusive
    foo: int

    # any number
    bar: int

    # any number from 0 to 10, inclusive
    baz: float

    # the intermediate values of the calculation
    values: List[float]

    # how many values this can "calculate" per second
    values_per_second: int = field(default=100)

    error: Optional[Error] = field(default=None)
    cancelled_at: datetime = field(default=None)

    @staticmethod
    def random():
        calc_type = random.choice(list(calc_types.keys()))
        foo = random.randint(-10, 10)
        bar = random.randint(-10, 10)
        baz = random.randint(0, 10)
        values = calc_values(calc_type, foo, bar, baz)
        return Calculation(id=uuid4(),
                           calc_type=calc_type,
                           started_at=datetime.now(),
                           foo=foo,
                           bar=bar,
                           baz=baz,
                           values=values,
                           values_per_second=random.randint(50, 300))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.summary(datetime.now()))
    
    @property
    def total_steps(self):
        return len(self.values)

    def cancelled(self, at):
        """
        Returns a copy of this Calculation cancelled at time `at`.
        """
        return replace(self, cancelled_at=at)

    def errored(self, error: str, at: datetime):
        """
        Returns a copy of this Calculation errored at time `at`.
        """
        return replace(self, error=Error(error=error, errored_at=at))

    def values_at_time(self, time):
        """
        Returns the list of intermediate values "calculated" by time `time`,
        given `values_per_second`. If this was cancelled or errored,
        returns only the values up to that point.
        """
        return self.values[0:self.step_at_time(time)]

    def value_at_time(self, time):
        return self.values[self.step_at_time(time)]

    def step_at_time(self, time):
        at = self.stopped_at(time) or time
        elapsed = at - self.started_at
        step_at_elapsed = elapsed.seconds * self.values_per_second
        return min(step_at_elapsed, len(self.values)) - 1

    def errored_at(self):
        return self.error.errored_at if self.error else None

    def stopped_at(self, time):
        return self.completed_at(time) or self.cancelled_at or self.errored_at() or None

    @property
    def time_to_calculate(self):
        return max_seconds

    def completed_at(self, time):
        would_complete_at = self.started_at + timedelta(seconds=self.time_to_calculate)
        can_complete = not (self.errored_at() or self.cancelled_at)
        return would_complete_at if can_complete and would_complete_at <= time else None

    def fraction_complete(self, time):
        step = self.step_at_time(time)
        return step / self.total_steps
    
    def summary(self, time):
        return py_.omit(self.detail(time), 'values')

    def detail(self, time):
        return {
            **asdict(self),
            'values': self.values_at_time(time),
            'value': self.value_at_time(time),
            'completed_at': self.completed_at(time),
            'cancelled_at': self.cancelled_at,
            'error': self.error or None,
            'fraction_complete': self.fraction_complete(time)
        }


def random_true(frequency):
    return random.choices([True, False], weights=[1, frequency])[0]

def random_error():
    if random_true(error_frequency):
        return random.shuffle(choice(errors))

def calc_values(calc_type, foo, bar, baz):
    return [calc_y(x,
                   calc_type=calc_type,
                   foo=foo,
                   bar=bar,
                   baz=baz) for x in calc_xs()]

def calc_xs():

    x_min = -10.0
    x_max = 10.0

    domain = x_max - x_min
    step_size = 1 / resolution
    steps = ceil(domain / step_size)
    return (x_min + (n * step_size) for n in range(0, steps))

# todo: work these out
calc_types = {
    "blue": lambda x, v: v * sin(x),
    "green": lambda x, v: v * cos(x),
    "purple": lambda x, v: v + (x),
    "yellow": lambda x, v: v - (x)
}

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
    calc = calc_types[calc_type]
    v = (foo * sin(x)) * cos(bar * x)
    return calc(x, v)
