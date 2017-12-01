import math
import random
from abc import ABCMeta, abstractmethod


class Cell:
    def __init__(self, x, y):
        self.y = y
        self.x = x

    def distance(self, other):
        return math.hypot(self.x - other.x, self.x - other.x)

    def closest(self, others):
        return min(others, key=lambda other: self.distance(other))

    def towards(self, other, limit: int):
        x = self.x
        y = self.y

        for _ in range(limit):
            if x < other.x:
                x += 1
            if x > other.x:
                x -= 1

            if y < other.y:
                y += 1
            if y > other.y:
                y -= 1

        return Cell(x, y)

    def towards_one_of(self, others, limit: int):
        return self.towards(self.closest(others), limit)

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Cell):
            return Cell(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __hash__(self):
        return hash('{},{}'.format(self.x, self.y))

    def __repr__(self):
        return '{},{}'.format(self.x, self.y)

    def as_tuple(self):
        return self.x, self.y


class Pool(metaclass=ABCMeta):
    def __init__(self):
        self.creatures = {}

    def add(self, creature):
        cell = self.random_cell()
        if self.cell_is_free(cell):
            self.creatures[cell] = creature
            return True
        return False

    def remove(self, creature):
        cell = list(self.creatures.keys())[list(self.creatures.values()).index(creature)]
        self.creatures.pop(cell)

    def move_creature(self, creature, delta_x, delta_y):
        cell = list(self.creatures.keys())[list(self.creatures.values()).index(creature)]
        new_cell = Cell(cell.x + delta_x, cell.y + delta_y)

        if new_cell not in self.creatures and self.cell_in_bounds(new_cell):
            self.creatures[new_cell] = self.creatures.pop(cell)
            print('{} moved from {} to {}'.format(creature, cell, new_cell))

    def cell_is_free(self, cell):
        return cell not in self.creatures

    @abstractmethod
    def cell_in_bounds(self, cell): ...

    @abstractmethod
    def random_cell(self): ...

    def _cell_repr(self, x, y):
        cell = Cell(x, y)
        return self.creatures[cell].get_sign() if cell in self.creatures else ' '


class RectanglePool(Pool):
    def __init__(self, w, h):
        super().__init__()
        self.w = w
        self.h = h

    def random_cell(self):
        x = random.randrange(self.w)
        y = random.randrange(self.h)
        return Cell(x, y)

    def cell_in_bounds(self, cell):
        return 0 <= cell.x < self.w and 0 <= cell.y < self.h

    def __repr__(self):
        border = ' ' + ''.join(['-' for _ in range(self.w)]) + ' '

        result = [border]
        for y in range(self.h):
            row = []
            for x in range(self.w):
                row.append(self._cell_repr(x, y))
            result.append('|' + ''.join(row) + '|')
        result.append(border)

        return '\n'.join(result)


class HexagonalPool(Pool):
    def __init__(self, size):
        super().__init__()
        self.size = size

    def random_cell(self):
        y = random.randrange(self.size)
        start, end = self.row_bounds(y)
        x = random.randrange(start, end)
        return Cell(x, y)

    def cell_in_bounds(self, cell):
        start, end = self.row_bounds(cell.y)
        return start <= cell.x < end and 0 <= cell.y < self.size

    def row_bounds(self, y):
        half = self.size // 2
        start = abs(half - y)
        end = (self.size * 2 - 1 - start)

        return start, end

    def __repr__(self):
        half = self.size // 2
        horizontal_border = ' ' * (half + 2) + '-' * (self.size - 2) + ' ' * (half + 2)

        result = [horizontal_border]
        for y in range(self.size):
            row = []
            start, end = self.row_bounds(y)
            for x in range(start, end):
                row.append(self._cell_repr(x, y))
            outside = ' ' * start
            left_border, right_border = self.vertical_borders(y)
            result.append(outside + left_border + ''.join(row) + right_border + outside)
        result.append(horizontal_border)

        return '\n'.join(result)

    def vertical_borders(self, y):
        half = self.size // 2
        if y < half:
            left_border = '/'
            right_border = '\\'
        elif y > half:
            left_border = '\\'
            right_border = '/'
        else:
            left_border = '('
            right_border = ')'

        return left_border, right_border


class Observable:
    def __init__(self):
        self.listeners = {}

    def add_event_listener(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit_event(self, event_name, data=None):
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener(data)

    def remove_all_listeners(self):
        self.listeners.clear()


class Fish(Observable):
    counter = 0

    def __init__(self, endurance, gestation, generation_size):
        super().__init__()
        self.max_endurance = endurance
        self.endurance = self.max_endurance
        self.gestation = gestation
        self.generation_size = generation_size
        self.turns_to_next_child = self.gestation

        self.id = Fish.counter + 1
        Fish.counter += 1

    def turn(self):
        self.gestate()
        self.move()
        self.exhaust()

    def gestate(self):
        self.turns_to_next_child -= 1
        if self.turns_to_next_child <= 0:
            self.breed()

    def exhaust(self):
        self.endurance -= 1
        if self.endurance <= 0:
            self.die()
            print('{} died by itself'.format(self))

    def breed(self):
        self.turns_to_next_child = self.gestation
        children = [self.make_child() for _ in range(self.generation_size)]
        self.emit_event('reproduce', children)
        print('{} born {} children'.format(self, len(children)))

    @abstractmethod
    def make_child(self): ...

    def die(self):
        self.emit_event('die')
        self.remove_all_listeners()

    @abstractmethod
    def move(self): ...

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)

    @classmethod
    def get_sign(cls):
        return 'X'


class Victim(Fish):
    def __init__(self, endurance, gestation, generation_size):
        super().__init__(endurance, gestation, generation_size)
        self.generation_size = generation_size
        self.move_range = 1

    def make_child(self):
        return Victim(self.endurance, self.gestation, self.generation_size)

    def move(self):
        delta_x = random.randrange(self.move_range * 2 + 1) - 1
        delta_y = random.randrange(self.move_range * 2 + 1) - 1
        self.emit_event('move', (delta_x, delta_y))

    @classmethod
    def get_sign(cls):
        return 'V'


class Predator(Fish):
    def __init__(self, endurance, gestation, pool: Pool):
        super().__init__(endurance, gestation, 1)
        self.pool = pool
        self.move_range = 2
        self.can_eat = (Victim, Hybrid)

    def move(self):
        predator_cell = list(self.pool.creatures.keys())[list(self.pool.creatures.values()).index(self)]
        victim_cells = [k for k, v in self.pool.creatures.items() if isinstance(v, self.can_eat)]

        if victim_cells:
            target_cell = predator_cell.towards_one_of(victim_cells, self.move_range)

            if target_cell in victim_cells:
                victim = self.pool.creatures[target_cell]
                self.eat(victim)
                print('{} eaten {} at {}'.format(self, victim, target_cell))

            next_move = (target_cell - predator_cell).as_tuple()
            self.emit_event('move', next_move)

    def eat(self, victim):
        victim.die()
        self.endurance = self.max_endurance

    def make_child(self):
        return Predator(self.max_endurance, self.gestation, self.pool)

    @classmethod
    def get_sign(cls):
        return 'P'


class Hybrid(Predator):
    def __init__(self, endurance, gestation, pool: Pool):
        super().__init__(endurance, gestation, 1)
        self.pool = pool
        self.move_range = 2
        self.can_eat = (Victim,)

    def make_child(self):
        return Hybrid(self.max_endurance, self.gestation, self.pool)

    @classmethod
    def get_sign(cls):
        return 'H'


class Game:
    def __init__(self, pool: Pool, predators_count, victims_count, predator_endurance, reproduction_period,
                 victim_lifespan, victim_generation_size):
        self.pool = pool

        for _ in range(victims_count):
            hybrid = Victim(victim_lifespan, reproduction_period, victim_generation_size)
            self.add(hybrid)

        for _ in range(victims_count):
            hybrid = Hybrid(victim_lifespan, reproduction_period, self.pool)
            self.add(hybrid)

        for _ in range(predators_count):
            predator = Predator(predator_endurance, reproduction_period, self.pool)
            self.add(predator)

    def add(self, creature):
        if self.pool.add(creature):
            creature.add_event_listener('die', lambda _: self.pool.remove(creature))
            creature.add_event_listener('move', lambda move: self.pool.move_creature(creature, *move))
            creature.add_event_listener('reproduce', lambda children: [self.add(child) for child in children])

    def turn(self):
        for creature in self.pool.creatures.copy().values():  # create a copy because the dictionary may change during iteration
            if creature in self.pool.creatures.values():  # check if creature is still alive (it might be eaten by a predator)
                creature.turn()


# first_pool = RectanglePool(10, 5)
second_pool = HexagonalPool(7)
game = Game(second_pool, 1, 4, 4, 5, 10, 3)
for turn in range(20):
    print('\nturn #{}'.format(turn))
    print(game.pool)
    game.turn()
