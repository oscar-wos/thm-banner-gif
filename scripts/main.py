#!/usr/bin/env python3
import os
import re
import glob
import time
import base64
import numpy
import asyncio
import requests
from flags import _flags
from logger import _logger
from tmp import _tmp
from translations import _t
from pyppeteer import launch
from PIL import Image


def gen_frame(path):
    im = Image.open(path)
    alpha = im.getchannel('A')

    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    im.paste(255, mask)
    im.info['transparency'] = 255

    return im


def gen(tmp):
    path = os.path.abspath(os.path.join(tmp, 'screenshots/trimmed'))
    frames = []

    for frame in glob.glob(f'{path}/*.png'):
        frames.append(gen_frame(frame))

    frame_one = frames[0]
    frame_one.save('thm.gif', append_images=frames,
                   save_all=True, duration=100, loop=0, optimize=False)
    _logger.log(_t.t('success'))


def trim_frame(path, output):
    image = Image.open(path)
    image.load()

    image_data = numpy.asarray(image)
    image_data_bw = image_data.max(axis=2)
    non_empty_columns = numpy.where(image_data_bw.max(axis=0) > 0)[0]
    non_empty_rows = numpy.where(image_data_bw.max(axis=1) > 0)[0]
    c = (min(non_empty_rows), max(non_empty_rows), min(
        non_empty_columns), max(non_empty_columns))

    image_data_new = image_data[c[0]:c[1]+1, c[2]:c[3]+1, :]

    new_image = Image.fromarray(image_data_new)
    new_image.save(output)


async def fetch_frames(tmp):
    path = os.path.abspath(os.path.join(tmp, './html/index.html'))

    data = {'omitBackground': True, 'clip': {
        'x': 0, 'width': 300, 'y': 0, 'height': 100}}

    _logger.log(_t.t('launching_html'))
    browser = await launch({'headless': 'false'})
    page = await browser.newPage()
    _logger.log(_t.t('success'))

    _logger.log(_t.t('fetching_html', {'path': path}))
    await page.goto(f'file://{path}')
    _logger.log(_t.t('success'))

    _logger.log(_t.t('generating_screenshots'))
    for i in range(100):
        data['path'] = os.path.abspath(
            os.path.join(tmp, f'screenshots/{i}.png'))
        await page.screenshot(data)
        trim_frame(data['path'], os.path.abspath(
            os.path.join(tmp, f'screenshots/trimmed/{i}.png')))
        time.sleep(0.1)
    _logger.log(_t.t('success'))

    _logger.log(_t.t('generating_gif'))
    gen(tmp)

    await browser.close()


def main():
    try:
        search = r'\"([A-z0-9+]*)\"'
        css_link = '<link rel="stylesheet" href="thm.css">\n'

        css_search = r'([\w\W]*)'
        css_search += r'<style scoped>([\w\W]*)<\/style>'
        css_search += r'([\w\W]*)<!--'

        lang = _flags.value(['--lang', '-l'])
        _t.load(lang) if lang else _t.load()
        tmp = _tmp.dir(['html', 'screenshots', 'screenshots/trimmed'])

        url = _flags.value(['--url', '-u'])

        if url is None:
            return _logger.log(_t.t('missing_flag', {
                'flag': '--url/-u <https://tryhackme.com/badge/>'}))

        _logger.log(_t.t('fetching_data', {'url': url}))
        r = requests.get(url)
        _logger.log(_t.t('success'))

        _logger.log(_t.t('searching_data'))
        r_result = re.search(search, r.text)

        if r_result is None:
            return _logger.log(_t.t('missing_data'))
        _logger.log(_t.t('success'))

        _logger.log(_t.t('decoding_data'))
        d = str(base64.b64decode(r_result.group(1)), 'UTF-8')
        _logger.log(_t.t('success'))

        _logger.log(_t.t('greping_data'))
        css_result = re.search(css_search, d)

        if css_result is None:
            return _logger.log(_t.t('missing_data'))
        _logger.log(_t.t('success'))

        path = os.path.abspath(os.path.join(tmp[0], './html/index.html'))
        _logger.log(_t.t('generating_data', {'path': path}))
        with open(path, 'w') as file:
            file.write(
                f'{css_link}\n{css_result.group(1)}{css_result.group(3)}')
        _logger.log(_t.t('success'))

        path = os.path.abspath(os.path.join(tmp[0], './html/thm.css'))
        _logger.log(_t.t('generating_data', {'path': path}))
        with open(path, 'w') as file:
            file.write(css_result.group(2))
        _logger.log(_t.t('success'))

        asyncio.get_event_loop().run_until_complete(fetch_frames(tmp[0]))

    except BaseException as ex:
        raise TypeError(ex)


if __name__ == '__main__':
    main()


# https://github.com/OSCAR-WOS/thm-banner-gif
