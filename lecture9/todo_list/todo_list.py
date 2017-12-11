class TodoList:
    def __init__(self, serializer):
        self.serializer = serializer

    def add(self, task):
        tasks = self.serializer.read()
        tasks.append({'name': task})
        self.serializer.write(tasks)
