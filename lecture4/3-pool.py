import random
import math
import functools


class Pool:
    def __init__(self, w, h, p, v, n, m, k, z):
        self.w = w
        self.h = h
        self.predator_endurance = n
        self.reproduction_period = m
        self.victim_lifespan = k
        self.victim_generation_size = z

        self.fish = {}

        for i in range(v):
            self.add_victim()

        for i in range(p):
            self.add_predator()

    def add_victim(self):
        x = random.randrange(self.w)
        y = random.randrange(self.h)
        if self.cell_is_free(x, y):
            victim = Victim(x, y, self)
            self.fish[self.format_cell(x, y)] = victim

    def add_predator(self):
        x = random.randrange(self.w)
        y = random.randrange(self.h)
        if self.cell_is_free(x, y):
            predator = Predator(x, y, self)
            self.fish[self.format_cell(x, y)] = predator

    def cell_is_free(self, x, y):
        cell = self.format_cell(x, y)
        return cell not in self.fish

    def remove(self, x, y):
        cell = self.format_cell(x, y)
        if cell in self.fish:
            del self.fish[cell]

    def turn(self):
        for fish in [*self.fish.values()]:
            fish.turn()

    def move_fish(self, from_x, from_y, to_x, to_y):
        from_cell = self.format_cell(from_x, from_y)
        to_cell = self.format_cell(to_x, to_y)

        self.fish[to_cell] = self.fish[from_cell]
        del self.fish[from_cell]

    @staticmethod
    def format_cell(x, y):
        return '{},{}'.format(x, y)

    def _cell_repr(self, x, y):
        cell = self.format_cell(x, y)
        if cell in self.fish:
            return 'P' if isinstance(self.fish[cell], Predator) else 'V'
        else:
            return ' '

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


class Fish:
    def __init__(self, x, y, endurance, pool: Pool):
        self.x = x
        self.y = y
        self.endurance = endurance
        self.pool = pool
        self.turns_to_next_child = self.pool.reproduction_period

    def turn(self):
        self.turns_to_next_child -= 1
        if self.turns_to_next_child <= 0:
            self.reproduce()
        self.move()
        self.endurance -= 1
        if self.endurance <= 0:
            self.die()

    def reproduce(self):
        self.turns_to_next_child = self.pool.reproduction_period

    def die(self):
        self.pool.remove(self.x, self.y)

    def move(self):
        pass

    def _do_move(self, x, y):
        self.pool.move_fish(self.x, self.y, x, y)
        self.x = x
        self.y = y


class Predator(Fish):
    def __init__(self, x, y, pool: Pool):
        super().__init__(x, y, pool.predator_endurance, pool)

    def reproduce(self):
        super().reproduce()
        self.pool.add_predator()

    def move(self):
        victim = self._closest_victim()

        def closer_cell():
            x = self.x
            if x < victim.x:
                x += 1
            if x > victim.x:
                x -= 1

            y = self.y
            if y < victim.x:
                y += 1
            if y > victim.x:
                y -= 1

            return x, y

        new_x, new_y = closer_cell()
        if self.pool.cell_is_free(new_x, new_y):
            super()._do_move(new_x, new_y)
        else:
            cell = self.pool.format_cell(new_x, new_y)
            if isinstance(self.pool.fish[cell], Victim):
                # eat
                self.pool.remove(new_x, new_y)
                self.endurance = pool.predator_endurance
                super()._do_move(new_x, new_y)

    def _closest_victim(self):
        def distance(victim):
            delta_x = self.x - victim.x
            delta_y = self.x - victim.x
            return math.sqrt(delta_x ** 2 + delta_y ** 2)

        def reducer(closest, victim):
            return victim if distance(victim) < distance(closest) else closest

        victims = filter(lambda f: isinstance(f, Victim), self.pool.fish.values())
        return functools.reduce(reducer, victims)

    def __repr__(self):
        return 'Predator({},{})'.format(self.x, self.y)


class Victim(Fish):
    def __init__(self, x, y, pool: Pool):
        super().__init__(x, y, pool.victim_lifespan, pool)

    def reproduce(self):
        super().reproduce()
        for i in range(self.pool.victim_generation_size):
            self.pool.add_victim()

    def move(self):
        delta_x = random.randrange(3) - 1
        delta_y = random.randrange(3) - 1
        x = self.x + delta_x
        y = self.y + delta_y

        in_bounds = 0 <= x < self.pool.w and 0 <= y < self.pool.h
        if in_bounds and self.pool.cell_is_free(x, y):
            super()._do_move(x, y)

    def __repr__(self):
        return 'Victim({},{})'.format(self.x, self.y)


pool = Pool(10, 5, 3, 8, 4, 4, 5, 2)
for i in range(10):
    print(pool)
    pool.turn()
