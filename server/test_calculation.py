from datetime import datetime
from server.calculation import Calculation, calc_xs, calc_y, calc_values

midnight = datetime(year=2022, month=1, day=1)

class TestStepAtTime:

    def test_step_at_time_0():
        pass

    def test_step_at_time_in_middle():
        pass

    def test_step_at_time_past_end():
        pass

class TestCompletedAt:

    def test_is_completed_at_time():
        pass

    def test_is_cancelled_at_time():
        pass

    def test_is_errored_at_time():
        pass

    def test_is_still_running():
        pass



