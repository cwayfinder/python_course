import math


class Triangle:
    def __init__(self, a: float, b: float, c: float):
        if a >= b + c or b >= a + c or c >= a + b:
            raise ValueError('Illegal parameters')

        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return 'Triangle({}, {}, {})'.format(self.a, self.b, self.c)

    def get_area(self):
        s = (self.a + self.b + self.c) / 2
        area = math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
        return round(area, 2)


t1 = Triangle(3, 4, 5)
print(t1)
print(t1.get_area())

t2 = Triangle(8, 2, 3)
