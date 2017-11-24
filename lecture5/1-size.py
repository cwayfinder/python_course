import numbers


class Size:
    units = {'km': 3, 'm': 0, 'sm': -2, 'mm': -3}

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __eq__(self, other):
        if isinstance(other, Size):
            return Size.to_base(self) == Size.to_base(other)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Size):
            value = Size.to_base(self) + Size.to_base(other)
            return Size(value, 'm')
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Size):
            value = Size.to_base(self) - Size.to_base(other)
            return Size(value, 'm')
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            value = Size.to_base(self) * other
            return Size(value, 'm')
        return NotImplemented

    @staticmethod
    def to_base(size):
        return size.value * (10 ** Size.units[size.unit])

    def __repr__(self):
        return 'Size({}{})'.format(self.value, self.unit)


print(Size(2, 'm') == Size(2, 'm'))
print(Size(2, 'm') == Size(200, 'sm'))
print(Size(2, 'm') == Size(2000, 'mm'))
print(Size(2, 'km') == Size(2000, 'm'))
print(Size(2, 'm') == Size(5, 'm'))
print(Size(2, 'km') + Size(5, 'm'))
print(Size(2, 'km') - Size(5, 'm'))
print(Size(2, 'km') * 4)
