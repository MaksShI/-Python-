import re


def index_page(request):
    return '200 OK', b'Hello from WSGI!'


def about_page(request):
    return '200 OK', b'About page'


class NotFoundPage:
    def __call__(self, request):
        return '404 Not Found', b'404 page not found'


routes = {
    '/': index_page,
    '/about': about_page
}


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'value'


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path in self.routes:
            controller = self.routes[path]
        else:
            controller = NotFoundPage()
        request = {}
        for front in self.fronts:
            front(request)
        code, body = controller()
        start_response(code, [('Content-Type', 'text/html')])
        return [body]


app_object = Application(routes, [secret_front, other_front])
