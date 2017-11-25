import random
import math
import functools
from abc import ABCMeta, abstractmethod


class Cell:
    def __init__(self, x, y):
        self.y = y
        self.x = x

    def distance(self, other):
        delta_x = self.x - other.x
        delta_y = self.x - other.x
        return math.sqrt(delta_x ** 2 + delta_y ** 2)

    def closest(self, others):
        def reducer(closest, other):
            return other if self.distance(other) < self.distance(closest) else closest

        return functools.reduce(reducer, others)

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
    @property
    @abstractmethod
    def fish(self):
        pass

    @abstractmethod
    def add(self, fish):
        pass

    @abstractmethod
    def remove(self, fish):
        pass

    @abstractmethod
    def move_fish(self, fish, x, y):
        pass


class RectanglePool(Pool):
    def __init__(self, w, h):
        self.w = w
        self.h = h

        self._fish = {}

    @property
    def fish(self):
        return self._fish

    def add(self, fish):
        cell = self.random_cell()
        if self.cell_is_free(cell):
            self.fish[cell] = fish
            return True
        return False

    def random_cell(self):
        x = random.randrange(self.w)
        y = random.randrange(self.h)
        return Cell(x, y)

    def cell_is_free(self, cell):
        return cell not in self.fish

    def cell_in_bounds(self, cell):
        return 0 <= cell.x < self.w and 0 <= cell.y < self.h

    def remove(self, fish):
        cell = list(self.fish.keys())[list(self.fish.values()).index(fish)]
        self.fish.pop(cell)

    def move_fish(self, fish, x, y):
        cell = list(self.fish.keys())[list(self.fish.values()).index(fish)]
        new_cell = Cell(cell.x + x, cell.y + y)

        if new_cell not in self.fish and self.cell_in_bounds(new_cell):
            self.fish[new_cell] = self.fish.pop(cell)
            print('{} moved from {} to {}'.format(fish, cell, new_cell))

    def _cell_repr(self, x, y):
        cell = Cell(x, y)
        return self.fish[cell].get_sign() if cell in self.fish else ' '

    def __repr__(self):
        border = '|' + ''.join(['-' for _ in range(self.w)]) + '|'

        result = [border]
        for y in range(self.h):
            row = []
            for x in range(self.w):
                row.append(self._cell_repr(x, y))
            result.append('|' + ''.join(row) + '|')
        result.append(border)

        return '\n'.join(result)


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

    def __init__(self, endurance, reproduction_period, generation_size):
        super().__init__()
        self.max_endurance = endurance
        self.endurance = self.max_endurance
        self.reproduction_period = reproduction_period
        self.generation_size = generation_size
        self.turns_to_next_child = self.reproduction_period

        self.id = Fish.counter + 1
        Fish.counter += 1

    def turn(self):
        self.turns_to_next_child -= 1
        if self.turns_to_next_child <= 0:
            self.reproduce()

        self.move()
        self.exhaust()

    def exhaust(self):
        self.endurance -= 1
        if self.endurance <= 0:
            self.die()
            print('{} died by itself'.format(self))

    def reproduce(self):
        self.turns_to_next_child = self.reproduction_period
        children = [self.make_child() for _ in range(self.generation_size)]
        self.emit_event('reproduce', children)
        print('{} born {} children'.format(self, len(children)))

    def make_child(self):
        pass

    def die(self):
        self.emit_event('die')
        self.remove_all_listeners()

    def move(self):
        pass

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)

    def get_sign(self):
        pass


class Victim(Fish):
    def __init__(self, endurance, reproduction_period, generation_size):
        super().__init__(endurance, reproduction_period, generation_size)
        self.generation_size = generation_size
        self.move_range = 1

    def make_child(self):
        return Victim(self.endurance, self.reproduction_period, self.generation_size)

    def move(self):
        delta_x = random.randrange(self.move_range * 2 + 1) - 1
        delta_y = random.randrange(self.move_range * 2 + 1) - 1
        self.emit_event('move', (delta_x, delta_y))

    def get_sign(self):
        return 'V'


class Predator(Fish):
    def __init__(self, endurance, reproduction_period, pool: Pool):
        super().__init__(endurance, reproduction_period, 1)
        self.pool = pool
        self.move_range = 2
        self.can_eat = (Victim, Hybrid)

    def move(self):
        predator_cell = list(self.pool.fish.keys())[list(self.pool.fish.values()).index(self)]
        victim_cells = [k for k, v in self.pool.fish.items() if isinstance(v, self.can_eat)]

        if victim_cells:
            target_cell = predator_cell.towards_one_of(victim_cells, self.move_range)

            if target_cell in victim_cells:
                victim = self.pool.fish[target_cell]
                self.eat(victim)
                print('{} eaten {} at {}'.format(self, victim, target_cell))

            next_move = (target_cell - predator_cell).as_tuple()
            self.emit_event('move', next_move)

    def eat(self, victim):
        victim.die()
        self.endurance = self.max_endurance

    def make_child(self):
        return Predator(self.max_endurance, self.reproduction_period, self.pool)

    def get_sign(self):
        return 'P'


class Hybrid(Predator):
    def __init__(self, endurance, reproduction_period, pool: Pool):
        super().__init__(endurance, reproduction_period, 1)
        self.pool = pool
        self.move_range = 2
        self.can_eat = (Victim,)

    def make_child(self):
        return Hybrid(self.max_endurance, self.reproduction_period, self.pool)

    def get_sign(self):
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

    def add(self, fish):
        if self.pool.add(fish):
            fish.add_event_listener('die', lambda _: self.pool.remove(fish))
            fish.add_event_listener('move', lambda move: self.pool.move_fish(fish, *move))
            fish.add_event_listener('reproduce', lambda children: [self.add(child) for child in children])

    def turn(self):
        for fish in self.pool.fish.copy().values():  # create a copy because the dictionary may change during iteration
            if fish in self.pool.fish.values():  # check if fish is still alive (it might be eaten by a predator)
                fish.turn()


first_pool = RectanglePool(10, 5)
game = Game(first_pool, 1, 4, 4, 5, 10, 3)
for i in range(20):
    print('\nturn #{}'.format(i))
    print(game.pool)
    game.turn()
