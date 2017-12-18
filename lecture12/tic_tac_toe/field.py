class Field:
    def __init__(self):
        self._data = [[' ' for _ in range(3)] for _ in range(3)]

    def set_symbol(self, x, y, symbol):
        """
        >>> f = Field()
        >>> f.set_symbol(0,0,'X')
        >>> f._data[0][0]
        'X'
        >>> f.set_symbol(0,0,'X')
        Traceback (most recent call last):
        ...
        ValueError
        """
        if self._data[x][y] != ' ':
            raise ValueError
        self._data[x][y] = symbol

    def game_over(self):
        return self._go_by_rows() or

    def _go_by_rows(self):
        """
        >>> f = Field()
        >>> f._go_by_rows()
        False
        >>> f._data[0] = ['X','X','X']
        >>> f._go_by_rows()
        True
        """
        return self._test_rows(self._data)

    def _go_by_cols(self):
        """
        >>> f = Field()
        >>> f._go_by_cols()
        False
        >>> f._data[0][0] = 'X'
        >>> f._data[1][0] = 'X'
        >>> f._data[2][0] = 'X'
        >>> f._go_by_cols()
        True
        """
        return self._test_rows(list(zip(*self._data)))

    def _go_by_diagonals(self):
        """
        >>> f = Field()
        >>> f._go_by_diagonals()
        False
        >>> f._data[0][0] = 'X'
        >>> f._data[1][1] = 'X'
        >>> f._data[2][2] = 'X'
        >>> f._go_by_diagonals()
        True
        >>> f = Field()
        >>> f._go_by_diagonals()
        False
        >>> f._data[0][2] = 'X'
        >>> f._data[1][1] = 'X'
        >>> f._data[2][0] = 'X'
        >>> f._go_by_diagonals()
        True
        """
        return self._all_in_row([self._data[i][i] for i in range(3)]) or self._all_in_row([self._data[i][i] for i in range(3)])

    @staticmethod
    def _test_rows(field):
        for row in field:
            if Field._all_in_row(row):
                return True
        return False

    def _is_draw_fame(self):
        for row in self._data:
            if ' ' in row:
                return False
        return False

    def __str__(self):
        return '\n'.join('|'.join(cell for cell in row) for row in self._data)

    @staticmethod
    def _all_in_row(row):
        return row[0] != ' ' and list(row) == [row[0]] * 3

