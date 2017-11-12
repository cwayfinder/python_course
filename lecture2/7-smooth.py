import functools


def smooth(dx: int):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(x):
            n = (f(x - dx), f(x), f(x + dx))
            return sum(n) / len(n)

        return wrapper

    return decorator


@smooth(2)
def get_area(x):
    return x * x


print(get_area(2.5))
