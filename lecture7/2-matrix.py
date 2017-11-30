class Matrix:
    def __init__(self, data):
        self._data = data

    def item(self, row_index, col_index):
        return self._data[row_index][col_index]

    def row(self, index):
        return self._data[index]

    def column(self, index):
        return [row[index] for row in self._data]

    def height(self):
        return len(self._data)

    def width(self):
        return len(self._data[0])

    def __repr__(self):
        return '\n'.join([str(row) for row in self._data])

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise NotImplemented

        if other.width() == self.width() and other.height() == self.height():
            result = []
            for row in range(self.height()):
                result.append([self.item(row, col) + other.item(row, col) for col in range(self.width())])
            return Matrix(result)

        return ValueError

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise NotImplemented

        if other.width() == self.width() and other.height() == self.height():
            result = []
            for row in range(self.height()):
                result.append([self.item(row, col) - other.item(row, col) for col in range(self.width())])
            return Matrix(result)

        return ValueError


m1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
m2 = Matrix([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
print(m1, '\n')
print(m2, '\n')
print(m1 + m2, '\n')
print(m1 - m2, '\n')
