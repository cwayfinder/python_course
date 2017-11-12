import functools


def factorial(n: int):
    return functools.reduce(lambda x, y: x * y, range(1, n + 1))


print(factorial(5))
