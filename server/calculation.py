import random
from math import sin, cos, ceil, floor
from uuid import uuid4, UUID
from typing import List, Optional
from dataclasses import dataclass, replace, asdict, field
from datetime import datetime, timedelta
from pydash import py_


def calc_xs():

    # number of x values per 1.0 along the x-axis
    resolution = 100
    
    x_min = -10.0
    x_max = 10.0

    domain = x_max - x_min
    step_size = 1 / resolution
    steps = ceil(domain / step_size)
    return [x_min + (n * step_size) for n in range(0, steps)]

calc_types = {
    "blue": lambda x, v: v * sin(x),
    "green": lambda x, v: v * cos(x),
    "purple": lambda x, v: v + (x),
    "yellow": lambda x, v: v - (x)
}

def calc_y(x, calc_type, foo, bar, baz):
    """Some visually interesting functions, 
    should the candidate be curious to visualize them
    """
    calc = calc_types[calc_type.lower()]
    v = (foo * sin(x)) * cos(bar * x) + baz
    return calc(x, v)


@dataclass(frozen=True)
class Error:
    errored_at: datetime
    error: str

@dataclass(frozen=True)
class Calculation:
    """Simulates a long-running calculation that updates a value
    over a period of time until it arrives at the final answer,
    like a differential equation.

    You give it the input values and the list of intermediate `values`,
    and `values_per_second` to dictate how quickly the calculation should
    simulate its progress, and at any given point it will provide
    its simulated state.
    """
    id: UUID

    user_id: UUID

    started_at: datetime

    inputs: dict

    # the intermediate values of the calculation
    values: List[float]

    # how many values this can "calculate" per second
    values_per_second: int

    error: Optional[Error] = field(default=None)
    cancelled_at: datetime = field(default=None)

    @staticmethod
    def create(user_id: str,
               inputs: dict,
               started_at: datetime = None,
               values_per_second: int = 100,
               xs = None,
               calc_y = calc_y):
        values = [calc_y(x, **inputs) for x in xs or calc_xs()]
        return Calculation(id=str(uuid4()),
                           user_id=user_id,
                           started_at=started_at or datetime.now(),
                           inputs=inputs,
                           values=values,
                           values_per_second=values_per_second)
        
    
    @staticmethod
    def random():        
        return Calculation.create(
            user_id=str(uuid4()),
            inputs={
                'calc_type': random.choice(list(calc_types.keys())),
                'foo': random.randint(-10, 10),
                'bar': random.randint(-10, 10),
                'baz': random.randint(0, 10),
            },
            values_per_second=random.randint(25, 200))

    def __repr__(self):
        return str(py_.omit(asdict(self), 'values'))
    
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
        elapsed_seconds = (at - self.started_at).seconds
        step_at_elapsed = floor(elapsed_seconds * self.values_per_second)
        return min(step_at_elapsed, len(self.values) - 1)

    @property
    def errored_at(self):
        return self.error.errored_at if self.error else None

    def stopped_at(self, time):
        return self.completed_at(time) or self.cancelled_at or self.errored_at or None

    @property
    def seconds_to_calculate(self):
        return ceil(len(self.values) / self.values_per_second)

    @property
    def will_complete_at(self):
        return self.started_at + timedelta(seconds=self.seconds_to_calculate)
    
    def completed_at(self, time):
        can_complete = not (self.errored_at or self.cancelled_at)
        return self.will_complete_at if can_complete and self.will_complete_at <= time else None
        
    def fraction_complete(self, time):
        if self.completed_at(time):
            return 100.0
        else:
            step = self.step_at_time(time)
            return float(step) / self.total_steps
    
    def summary(self, time):
        return {
            **py_.omit(self.detail(time), 'values'),
            'values': len(self.values)
        }

    def detail(self, time):
        return py_.omit({
            **asdict(self),
            **self.inputs,
            'values': self.values_at_time(time),
            'value': self.value_at_time(time),
            'completed_at': self.completed_at(time),
            'cancelled_at': self.cancelled_at,
            'error': self.error or None,
            'fraction_complete': self.fraction_complete(time)
        }, 'inputs')

