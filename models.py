from reusepatterns.prototypes import PrototypeMixin

class User:
    pass

class Teacher(User):
    pass

class Student(User):
    pass


class SimpleFactory:
    def __init__(self, types=None):
        self.types = types or {}

class UserFactory:
    types = {
        'student'
    }
