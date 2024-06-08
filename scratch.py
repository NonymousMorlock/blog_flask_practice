# Refresher on Decorators
from typing import Callable


def commenter(function) -> Callable:
    def closure(*args):
        result = function(*args)
        print(f'You called {function.__name__}(', end='')
        for index, arg in enumerate(args):
            print(arg, end=', ' if index != len(args) - 1 else ')\n')
        print(f'It returned: {result}')

    return closure


@commenter
def a_function(a, b, c):
    return a * b * c


a_function(1, 2, 3)
