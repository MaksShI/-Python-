class Application:

    def parse_input_data(self, data: str):
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    def parse_wsgi_input_data(self, data: bytes):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(selfself, env):
        content_length_data = env.get('CONTENT_LENGHT')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __init__(self, urlpatterns: dict, front_controller: list):
        self.urlpatterns = urlpatterns
        self.front_controller = front_controller

    def __call__(self, env, start_response):
        path = env['PATH_INFO']

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = {}
            for controller in self.front_controller:
                controller(request)
            code, text = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Not Found"]