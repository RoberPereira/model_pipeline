

class DotDict:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__dict__[key] = DotDict(**value)
            else:
                self.__dict__[key] = value
