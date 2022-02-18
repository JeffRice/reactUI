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
                             calc_y=lambda x: x,
                             values_per_second=100)

    
class TestStepAtTime:

    def test_step_at_time_0(self, calc):
        assert calc.step_at_time(calc.started_at) == 0

    def test_step_at_time_in_middle(self, calc):
        assert calc.step_at_time(calc.started_at + timedelta(seconds=3)) == 300

    def test_step_at_time_past_end(self, calc):
        assert calc.step_at_time(calc.started_at + timedelta(seconds=11)) == 999


class TestFractionComplete:

    def test_fraction_complete_0(self, calc):
        assert calc.fraction_complete(calc.started_at) == 0

    def test_fraction_complete_in_middle(self, calc):
        assert abs(calc.fraction_complete(calc.started_at + timedelta(seconds=3)) - 0.3) < .01

    def test_fraction_complete_past_end(self, calc):
        assert calc.fraction_complete(calc.started_at + timedelta(seconds=21)) > 0.99
    


def test_will_complete_at(calc):
    assert calc.will_complete_at == calc.started_at + timedelta(seconds=10)

def assert_completed_states(calc, *states):
    for seconds, completed in states:
        assert bool(calc.completed_at(calc.started_at + timedelta(seconds=seconds))) == completed

                            
class TestCompletedAt:
                        
    def test_runs_to_completion(self, calc):
        assert_completed_states(calc, (0, False), (4, False), (7, False), (11, True))


    def test_cancelled(self, calc):
        
        assert_completed_states(calc, (0, False), (4, False), (7, False), (11, True))

        cancelled = calc.cancelled(calc.started_at + timedelta(seconds=6))

        assert_completed_states(cancelled, (0, False), (4, False), (7, False), (11, False))

    def test_errored(self, calc):

        assert_completed_states(calc, (0, False), (4, False), (7, False), (11, True))

        errored = calc.errored("test error", calc.started_at + timedelta(seconds=6))

        assert_completed_states(errored, (0, False), (4, False), (7, False), (11, False))




