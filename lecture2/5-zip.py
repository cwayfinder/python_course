def my_zip(*iterables):
    length = min([len(i) for i in iterables])
    return [tuple(it[index] for it in iterables) for index in range(length)]


print(list(zip([1, 2, 3], ['a', 'b', 'c', 'd'])))
print(list(my_zip([1, 2, 3], ['a', 'b', 'c', 'd'])))
