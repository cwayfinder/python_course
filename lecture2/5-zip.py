def my_zip(*iterables):
    shortest = min([len(i) for i in iterables])

    for i in range(shortest):
        result = []
        for iterable in iterables:
            result.append(iterable[i])
        yield tuple(result)


print(list(zip([1, 2, 3], ['a', 'b', 'c', 'd'])))
print(list(my_zip([1, 2, 3], ['a', 'b', 'c', 'd'])))
