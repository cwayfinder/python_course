def sum_(n: int, state=[]):
    state.append(n)
    return sum(state)


print(sum_(3))
print(sum_(4))
print(sum_(5))
