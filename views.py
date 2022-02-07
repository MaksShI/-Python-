import logs.server_log_config
from templates import render
import logging
from logging_mod import ServerDecorate

SERVER_LOGGER = logging.getLogger('server')


@ServerDecorate()
def main_view(request):
    secret = request.get('secret-key', None)
    return '200 OK', render('index.html', secret=secret)


@ServerDecorate()
def about_view(request):
    return '200 OK', 'About'


@ServerDecorate()
def contact_view(request):
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Нам пришло сообщение от {email} с темой {title} и текстом {text}')
        return '200 OK', render('contact.html')
    else:
        return '200 OK', render('contact.html')


if __name__ == '__main__':

    contact_view()