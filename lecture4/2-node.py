class Node:
    def __init__(self, name):
        self.name = name
        self.children = {}

    def set(self, direction, child):
        self.children[direction] = child

    def get(self, direction):
        return self.children[direction]

    def move(self, path):
        direction = path[0]
        if len(path) > 1:
            return self.children[direction].move(path[1:])
        else:
            return self.children[direction]

    def __repr__(self):
        return 'Node({})'.format(self.name)


tree = Node('root')
a = Node('a')
b = Node('b')
c = Node('c')
d = Node('d')
e = Node('e')
f = Node('f')
g = Node('g')

tree.set('l', a)
tree.set('r', b)
a.set('l', c)
a.set('r', d)
c.set('l', e)
c.set('r', f)
e.set('l', g)

print(tree.move('l'))
print(tree.move('ll'))
print(tree.move('lll'))
