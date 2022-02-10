from MUA.CBV import CreateView, ListView
from logging_mod import Logger

from urllib.parse import unquote
from MUA import Application
import views
from models import TrainingSite, EmailNotifier, SmsNotifier
from templates import render

site = TrainingSite()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


def course_lists(request):
    logger.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=site.courses)


def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = unquote(data['name'])
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
            site.courses.append(course)
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = site.categories
        return context

    def create_obj(self, data: dict):
        name = unquote(data['name'])
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)


class CategoryListView(ListView):
    queryset = site.categories
    template_name = 'category_list.html'


class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = unquote(data['name'])
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        print(data)
        course_name = unquote(data['course_name'])
        course = site.get_course(course_name)
        student_name = unquote(data['student_name'])
        student = site.get_student(student_name)
        course.add_student(student)


def secret_controller(request):
    request['secret'] = 'secret'


urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contact/': views.contact_view,
    '/create-course/': create_course,
    '/course-list/': course_lists,
    '/create-category/': CategoryCreateView(),
    '/category-list/': CategoryListView(),
    '/student-list/': StudentListView(),
    '/create-student/': StudentCreateView(),
    '/add-student/': AddStudentByCourseCreateView(),
}

front_controllers = [
    secret_controller
]
app = Application(urlpatterns, front_controllers)


@app.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    print(request_params)
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


@app.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)


def secret_controller(request):
    request['secret_key'] = 'SECRET'


application = Application(urlpatterns, front_controllers)

# gunicorn main:application
