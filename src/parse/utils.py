from functools import reduce

def composition(*funcs):
    def wrapper(x):
        for func in funcs:
            x = func(x)
        return x
    return wrapper
