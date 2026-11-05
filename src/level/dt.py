import time
from contextlib import contextmanager

import config as c
from utils.singleton import Singleton


class Dt(metaclass=Singleton):
    def __init__(self):
        self.dt = 0
        self.prev_time = 0

    def tick(self):
        t_now = time.perf_counter()
        dt = t_now - self.prev_time
        self.dt = dt if dt < c.DT_MAX else 0
        self.prev_time = t_now

    def reset_dt(self):
        self.prev_time = time.perf_counter()
        self.dt = 0

    @contextmanager
    def forcepause(self):
        try:
            yield
        finally:
            self.reset_dt()