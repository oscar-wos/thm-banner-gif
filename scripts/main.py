#!/usr/bin/env python3

def main():
    try:
        from flags import _flags
        flag_lang = _flags.value(['--lang', '-l'])

    except ImportError:
        pass

    try:
        from translations import _translations
        _translations.load() if flag_lang is None else _translations.load(
            flag_lang)

    except ImportError:
        pass

    try:
        from tmp import _tmp
        _tmp.generate()

    except ImportError:
        pass


if __name__ == '__main__':
    main()


# https://github.com/OSCAR-WOS/python-boilerplate
