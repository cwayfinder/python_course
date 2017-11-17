import random


class Pool:
    def __init__(self, w, h, p, v, n, m, k, z):
        self.w = w
        self.h = h
        self.predator_endurance = n
        self.reproduction_period = m
        self.victim_lifespan = k
        self.victim_generation_size = z

        self.victims = {}
        for i in range(v):
            self.add_victim()

        self.predators = {}
        for i in range(p):
            self.add_predator()

    def add_victim(self):
        x = random.randrange(self.w)
        y = random.randrange(self.h)
        if self.cell_free(x, y):
            victim = Victim(x, y, self)
            self.victims[self._format_cell(x, y)] = victim

    def add_predator(self):
        x = random.randrange(self.w)
        y = random.randrange(self.h)
        if self.cell_free(x, y):
            predator = Predator(x, y, self)
            self.predators[self._format_cell(x, y)] = predator

    def cell_free(self, x, y):
        cell = self._format_cell(x, y)
        return cell not in self.victims and cell not in self.predators

    def remove(self, x, y):
        cell = self._format_cell(x, y)
        if cell in self.victims:
            del self.victims[cell]
        if cell in self.predators:
            del self.predators[cell]

    def turn(self):
        for victim in [*self.victims.values()]:
            victim.turn()
        for predator in [*self.predators.values()]:
            predator.turn()

    @staticmethod
    def _format_cell(x, y):
        return '{},{}'.format(x, y)

    def _cell_repr(self, x, y):
        cell = self._format_cell(x, y)
        if cell in self.predators:
            return 'P'
        elif cell in self.victims:
            return 'V'
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
    def __init__(self, x, y, pool: Pool):
        self.x = x
        self.y = y
        self.pool = pool
        self.turns_to_next_child = self.pool.reproduction_period

    def turn(self):
        self.turns_to_next_child -= 1
        if self.turns_to_next_child <= 0:
            self.reproduce()

    def reproduce(self):
        self.turns_to_next_child = self.pool.reproduction_period

    def die(self):
        self.pool.remove(self.x, self.y)


class Predator(Fish):
    def __init__(self, x, y, pool: Pool):
        super().__init__(x, y, pool)
        self.endurance = pool.predator_endurance

    def turn(self):
        super().turn()
        self.endurance -= 1
        if self.endurance <= 0:
            self.die()

    def reproduce(self):
        self.pool.add_predator()


class Victim(Fish):
    def __init__(self, x, y, pool: Pool):
        super().__init__(x, y, pool)
        self.lifespan = self.pool.victim_lifespan

    def turn(self):
        super().turn()
        self.lifespan -= 1

    def reproduce(self):
        for i in range(self.pool.victim_generation_size):
            self.pool.add_victim()


pool = Pool(10, 5, 3, 8, 4, 4, 5, 2)
print(pool)
pool.turn()
print(pool)
pool.turn()
print(pool)
pool.turn()
print(pool)
pool.turn()
print(pool)
pool.turn()
print(pool)
