from collections import defaultdict
from enum import Enum, auto
from functools import wraps


class Event:
    class When(Enum):
        BEFORE = auto()
        AFTER = auto()

    handlers = {
        When.BEFORE: defaultdict(list),
        When.AFTER: defaultdict(list),
    }

    @classmethod
    def listener(cls, event, when=When.BEFORE):
        def register_handler(f):
            cls.handlers[when][event].append(f)
            return f
        return register_handler

    @classmethod
    def fire(cls, event, when, *args, **kwargs):
        for handler in cls.handlers[when][event]:
            handler(*args, **kwargs)

    @classmethod
    def trigger(cls, *events):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for e in events:
                    cls.fire(e, cls.When.BEFORE, *args, **kwargs)

                result = func(*args, **kwargs)

                for e in events:
                    cls.fire(e, cls.When.AFTER, *args, **kwargs)

                return result
            return wrapper
        return decorator