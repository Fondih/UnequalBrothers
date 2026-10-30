_Registry = {}

def register(group):
    group = ["terrain"] + group

    def decorator(func):
        _Registry[func.__name__] = (func, group)
        return func
    return decorator

def get(name):
    return _Registry[name]

def get_all():
    return _Registry