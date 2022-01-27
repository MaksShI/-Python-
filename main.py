from MUA import Application
import views

urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
}


def secret_controller(request):
    request['secret_key'] = 'SECRET'


front_controllers = [
    secret_controller
]


application = Application(urlpatterns, front_controllers)

# gunicorn main:application