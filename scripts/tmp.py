import os


class Tmp():
    def __init__(self, path='./tmp/'):
        self._path = os.path.join(os.path.split(__file__)[0], path)
        self.delete(self._path)

    def __create(self, path):
        try:
            os.mkdir(path)
            return True

        except BaseException:
            return None

    def delete(self, path):
        """
        Usage: _tmp.delete('./tmp/')

        :path string:
        @return None
        """

        try:
            path = os.path.abspath(path)

            if os.path.isdir(path):
                with os.scandir(path) as scanner:
                    [self.delete(i) for i in scanner]

                os.rmdir(path)

            else:
                os.unlink(path)

        except BaseException:
            return None

    def dir(self, dirs=[]):
        """
        Usage: _tmp.dir(['html', 'html/img', 'screenshots'])

        :dirs list: optional
        @return list[string, None]
        """

        list = [os.path.join(self._path, i) for i in dirs]
        list.insert(0, self._path)

        for i, dir in enumerate(list):
            list[i] = list[i] if self.__create(dir) else None

        return list


_tmp = Tmp()


# https://github.com/OSCAR-WOS/python-boilerplate
