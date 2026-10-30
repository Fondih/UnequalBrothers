import time
from contextlib import contextmanager

import config as c


class Dt:
    _instance = None

    def __init__(self):
        if Dt._instance is not None:
            raise RuntimeError("Dt already exists - use Dt.get_instance() instead")

        self.dt = 0
        self.prev_time = 0
        Dt._instance = self

    def tick(self):
        t_now = time.perf_counter()
        dt = t_now - self.prev_time
        self.dt = dt if dt < c.DT_MAX else 0
        self.prev_time = t_now

    def get_dt(self):
        return self.dt

    def reset_dt(self):
        self.prev_time = time.perf_counter()
        self.dt = 0

    @contextmanager
    def forcepause(self):
        try:
            yield
        finally:
            self.reset_dt()

    @classmethod
    def get_instance(cls):
        return cls._instance