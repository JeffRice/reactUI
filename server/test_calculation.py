import pytest
from datetime import datetime, timedelta
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

                            
class TestCompletedAt:

    def test_is_completed_at_time(self, calc):
        pass

    def test_is_cancelled_at_time(self):
        pass

    def test_is_errored_at_time(self):
        pass

    def test_is_still_running(self):
        pass



