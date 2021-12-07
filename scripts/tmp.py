import os


class Tmp():
    def __init__(self, path='./tmp/'):
        self._path = path
        self._path_full = os.path.join(os.path.split(__file__)[0], self._path)
        self.delete(self.path_full)

    def delete(self, path):
        if not os.path.exists(path):
            return

        if os.path.isdir(path):
            with os.scandir(path) as it:
                for item in it:
                    self.delete(item.path)

            os.rmdir(path)

        else:
            os.unlink(path)

    def create(self, path):
        try:
            os.mkdir(path)

        except BaseException:
            return None

        return path

    def generate(self, directory_list=[]):
        """
        Usage: _tmp.generate(['html', 'html/img', 'screenshots'])

        :directory_list array:
        @return array[string, None]
        """

        list = [os.path.join(self.path_full, item) for item in directory_list]
        list.insert(0, self.path_full)

        for i, dir in enumerate(list):
            list[i] = list[i] if self.create(dir) else None

    @property
    def path(self):
        return self._path

    @property
    def path_full(self):
        return self._path_full


_tmp = Tmp()


# https://github.com/OSCAR-WOS/python-boilerplate
