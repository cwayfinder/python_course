class LazyList:
    def __init__(self, size=0):
        self.data = list(range(size))

    def __getitem__(self, index):
        if index >= len(self.data):
            self.__init__(index + 1)
        return self.data[index]


l1 = LazyList()
print(l1[6])
