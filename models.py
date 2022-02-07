from reuspatterns.prototypes import PrototypeMixin


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
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class Course(PrototypeMixin):
    def __init__(self, name):
        self.name = name


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class TrainingSite:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []

    def create_user(self, type_):
        return UserFactory.create(type_)

    def create_course(self, type_, name):
        return CourseFactory.create(type_, name)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item

        return None
