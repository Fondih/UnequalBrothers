_Registry = {}

def spec_menu(menu):
    def decorator(func):
        _Registry[func] = menu
        return menu
    return decorator

def get(func):
    return _Registry[func]

def get_all():
    return _Registry