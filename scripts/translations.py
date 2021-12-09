import os
import json


class Translations(dict):
    def __init__(self, path='../translations'):
        self._path = os.path.join(os.path.split(__file__)[0], path)
        self.load()

    def __ingest(self, path):
        try:
            with open(path) as file:
                return json.load(file)

        except BaseException:
            return None

    def load(self, lang='en'):
        """
        Usage: _t.load('es')

        :lang string: optional
        @return None
        """

        path = os.path.join(self._path, f'{lang}.json')
        self = self.__ingest(path)

    def t(self, phrase='', data={}):
        """
        Usage: _t.t('usage', {'file_name': '.py', 'flags': ''})

        :phrase string:
        :data object: optional
        @return string, None
        """

        try:
            if phrase in self:
                translation = self[phrase]

            else:
                path = os.path.join(self._path, 'en.json')
                translation = self.__ingest(path)[phrase]

            return translation.format_map(data)

        except BaseException:
            raise TypeError(
                f'{self._path}/ translation or data not found ({phrase})')

        return None


_t = Translations()


# https://github.com/OSCAR-WOS/python-boilerplate
