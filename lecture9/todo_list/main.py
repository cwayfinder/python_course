import configparser

from lecture9.todo_list.todo_list import TodoList
from lecture9.todo_list.serializer import create


c = configparser.ConfigParser()
c.read('main.ini')
serializer = create(c['Serializer']['format'])

t1 = TodoList(serializer)
t1.add('finish task 1')
