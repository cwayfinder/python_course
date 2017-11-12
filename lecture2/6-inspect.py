import functools


def inspect(func):
    def format_arguments(args, kwargs):
        delimiter = ', '
        positioned = delimiter.join([str(i) for i in args])
        named = delimiter.join([str(kwargs[i]) for i in kwargs])
        return delimiter.join([i for i in (positioned, named) if i])

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arguments = format_arguments(args, kwargs)
        result = func(*args, **kwargs)
        print(func.__name__ + '(' + arguments + ') -> ' + str(result))
        return result

    return wrapper


# Examples

@inspect
def get_area(x):
    return x * x


@inspect
def test_func(a, b, c, k, m):
    return 42


get_area(5)
test_func(5, 6, 7, k=11, m=12)
