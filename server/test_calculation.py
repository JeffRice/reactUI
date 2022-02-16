import pytest
from datetime import datetime, timedelta
from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime
import time
from server.calculation import Calculation, calc_xs, calc_y

midnight = datetime(year=2022, month=1, day=1)

@pytest.fixture
def calc():
    yield Calculation.create(user_id=uuid4(),
                             inputs={},
                             xs=list(range(1000)),
                             calc_y=lambda x: x)

    
class TestStepAtTime:

    def test_step_at_time_0(self, calc):
        assert calc.step_at_time(calc.started_at) == 0

    def test_step_at_time_in_middle(self, calc):
        assert calc.step_at_time(calc.started_at + timedelta(seconds=3)) == 300

    def test_step_at_time_past_end(self, calc):
        assert calc.step_at_time(calc.started_at + timedelta(seconds=11)) == 999


@dataclass
class States:
    seconds: int
    completed: bool
    cancelled: bool
    errored: bool


def assert_states(calc, *states):
    for state in states:
        assert bool(calc.completed_at(calc.started_at + timedelta(seconds=state.seconds))) == state.completed
        assert bool(calc.cancelled_at) == state.cancelled
        assert bool(calc.errored_at()) == state.errored

                            
class TestCompletedAt:
                        
    def test_runs_to_completion(self, calc):
        assert_states(calc,
                      States(seconds=5, completed=False, cancelled=False, errored=False),
                      States(seconds=7, completed=False, cancelled=False, errored=False),
                      States(seconds=11, completed=True, cancelled=False, errored=False))

    def test_cancelled(self, calc):

        assert_states(calc,
                      States(seconds=5, completed=False, cancelled=False, errored=False),
                      States(seconds=7, completed=False, cancelled=False, errored=False),
                      States(seconds=11, completed=True, cancelled=False, errored=False))

        cancelled = calc.cancelled(calc.started_at + timedelta(seconds=6))

        assert_states(cancelled,
                      States(seconds=5, completed=False, cancelled=False, errored=False),
                      States(seconds=7, completed=False, cancelled=True, errored=False),
                      States(seconds=11, completed=False, cancelled=True, errored=False))        

    def test_errored(self, calc):

        assert_states(calc,
                      States(seconds=5, completed=False, cancelled=False, errored=False),
                      States(seconds=7, completed=False, cancelled=False, errored=False),
                      States(seconds=11, completed=True, cancelled=False, errored=False))

        errored = calc.errored("test error", calc.started_at + timedelta(seconds=6))

        assert_states(errored,
                      States(seconds=5, completed=False, cancelled=False, errored=False),
                      States(seconds=7, completed=False, cancelled=False, errored=True),
                      States(seconds=11, completed=False, cancelled=False, errored=True))        




