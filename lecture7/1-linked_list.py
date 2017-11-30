class LinkedList:
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next
        self._len = 1 if value else 0

    def add(self, value):
        if self.next is None:
            self.next = LinkedList(value)
        else:
            self.next.add(value)
        self._len += 1

    def __iter__(self):
        item = self
        while item.next:
            yield item.value
            item = item.next
        yield item.value

    def __len__(self):
        return self._len

    def __repr__(self):
        return str([i for i in self])


l = LinkedList(5)
l.add(6)
l.add(7)
l.add(8)
print(l)
print('len', len(l))

for i in l:
    print(i)
