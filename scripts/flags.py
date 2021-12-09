import re
import sys


class Flags(dict):
    def __init__(self):
        self.__load()

    def __search(self, search='', arg=''):
        search_result = re.search(search, arg)

        if search_result:
            return search_result.group(0)

    def __load(self):
        for i, arg in enumerate(sys.argv[1:]):
            search = [r'--([A-z]*)$',  r'-([A-z])$']
            search_result = self.__search(
                search[0], arg) or self.__search(search[1], arg)

            if search_result:
                self[search_result.lower()] = i + 1

    def flag(self, flag, value=False):
        """
        Usage: _flags.flag('-v')

        :flag string:
        :value bool: optional
        @return True, tuple('{flag_name}', '{flag_value}'), None
        """
        try:
            index = self[flag.lower()]

            if value:
                return (sys.argv[index], sys.argv[index + 1])

            return True

        except BaseException:
            return None

    def value(self, values=[]):
        """
        Usage: _flags.value(['--lang', '-l'])

        :values list:
        @return string, None
        """
        for flag in values:
            value = self.flag(flag, True)

            if isinstance(value, tuple):
                return value[1]

        return None


_flags = Flags()


# https://github.com/OSCAR-WOS/python-boilerplate
