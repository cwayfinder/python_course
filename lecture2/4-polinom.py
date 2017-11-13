def gen_pol(vector):
    def f(x):
        s = 0
        for index, item in enumerate(reversed(vector)):
            s += item * (x ** index)
        return s

    return f


print(gen_pol([1, 1, 1])(1))
