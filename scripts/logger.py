import os
import datetime


class Logger():
    def __init__(self, path='./tmp/log.txt'):
        self._path = os.path.join(os.path.split(__file__)[0], path)

    def log(self, message):
        """
        Usage: _logger.log(f'Failled to specify {flag} flag, try again')

        :message string:
        @return None
        """

        timestamp = datetime.datetime.now()
        message = f'{timestamp}: {message}'
        print(message)

        try:
            with open(self._path, 'a') as file:
                message = message if message.endswith('\n') else f'{message}\n'
                file.write(message)

        except BaseException:
            pass

        return None


_logger = Logger()


# https://github.com/OSCAR-WOS/python-boilerplate
