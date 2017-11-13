import functools
import operator


def factorial(n: int):
    return functools.reduce(operator.mul, range(1, n + 1))


print(factorial(5))
