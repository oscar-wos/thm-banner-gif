import re
import sys


class Flags:
    def __init__(self):
        self._lookup = {}
        self.load()

    def search_flag(self, search='', arg=''):
        search_result = re.search(search, arg)

        if search_result:
            return search_result.group(0)

    def load(self):
        for i, arg in enumerate(sys.argv[1:]):
            search = [r'--([A-z]*)$',  r'-([A-z])$']
            search_result = self.search_flag(
                search[0], arg) or self.search_flag(search[1], arg)

            if search_result:
                self._lookup[search_result.lower()] = i + 1

    def flag(self, flag, value=False):
        """
        Usage: _flags.flag('-v')

        :flag string:
        :value bool: optional
        @return True, None, tuple('{flag_name}', '{flag_value}')
        """
        try:
            index = self._lookup[flag]

            if value:
                return (sys.argv[index], sys.argv[index + 1])

            return True

        except BaseException:
            return None

    def value(self, values=[]):
        """
        Usage: _flags.value(['--lang', '-l'])

        :values array:
        @return string, None
        """
        for flag in values:
            value = self.flag(flag, True)

            if isinstance(value, tuple):
                return value[1]

        return None

    @property
    def lookup(self):
        return self._lookup


_flags = Flags()


# https://github.com/OSCAR-WOS/python-boilerplate
