from logging_mod import Logger


from MUA import Application
import views
from models import TrainingSite
from templates import render

site = TrainingSite()
logger = Logger('main')


def main_view(request):
    logger.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=site.courses)


def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        course = site.create_course('record', name)
        site.courses.append(course)
        return '200 OK', render('course_list.html')
    else:
        return '200 OK', render('course_list.html')


def copy_course(request):
    request_params = request['request_params']
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)



urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contact/': views.contact_view,
    '/copy-course/': copy_course
}


def secret_controller(request):
    request['secret_key'] = 'SECRET'


front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)

# gunicorn main:application
