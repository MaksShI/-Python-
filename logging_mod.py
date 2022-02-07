from reuspatterns.singlestones import SingletonByName
import logging

SERVER_LOGGER = logging.getLogger('server')


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log--->', text)


class ServerDecorate:
    def __call__(self, func):
        def log(*args, **kwargs):
            SERVER_LOGGER.debug(
                f'Была активирована функция {func.__name__} '
                f'Аргументы функции  {args}, {kwargs} '
                f'Функция была вызвана из модуля {func.__module__}', stacklevel=2)

            res = func(*args, **kwargs)
            return res

        return log
