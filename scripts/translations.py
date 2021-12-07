import os
import json


class Translations():
    def __init__(self, path='../translations'):
        self._translations = {}
        self._translations_en = None
        self._path = os.path.join(os.path.split(__file__)[0], path)
        self.load()

    def injest(self, path):
        try:
            with open(path) as file:
                return json.load(file)

        except BaseException:
            return None

    def load(self, lang='en'):
        """
        Usage: _translations.load('es')

        :lang string: optional
        @return None
        """
        path = os.path.join(self._path, f'{lang}.json')
        self._translations = self.injest(path)

    def t(self, phrase='', data={}):
        """
        Usage: _translations.t('usage', {'file_name': '.py', 'flags': ''})

        :phrase string:
        :data object: optional
        @return string, None
        """
        try:
            if phrase in self._translations:
                translation = self._translations[phrase]

            elif self.__dict__['_translations_en'] is None:
                path = os.path.join(self._path, 'en.json')
                self._translations_en = self.injest(path)

                translation = self._translations_en[phrase]

            return translation.format_map(data)

        except TypeError:
            raise TypeError(
                f'{self._path}/ translation_not_found ({phrase})')

        except KeyError as ex:
            data = {'var': ex, 'phrase': phrase}
            print(self.t('t_not_found_data', data))

        return None

    @property
    def translations(self):
        return self._translations

    @property
    def path(self):
        return self._path


_translations = Translations()


# https://github.com/OSCAR-WOS/python-boilerplate
