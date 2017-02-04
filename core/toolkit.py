# -*- coding: utf-8 -*-

#
# basicRAT toolkit module
# https://github.com/vesche/basicRAT
#

import datetime
import os
import urllib
import zipfile


# def id(platform):
#    return 'foo'


# def screenshot(platform):
#    if platform.startswith('win') or platform.startswith('darwin'):
#        from PIL import ImageGrab
#    elif platform.startswith('linux'):
#        return
#    else:
#        return 'Platform unsupported.'


# def sysinfo(platform):
#     return 'bar'


def unzip(f):
    if os.path.isfile(f):
        try:
            with zipfile.ZipFile(f) as zf:
                zf.extractall('.')
                return 'File {} extracted.'.format(f)
        except zipfile.BadZipfile:
            return 'Error: Failed to unzip file.'
    else:
        return 'Error: File not found.'


def wget(url):
    fname = url.split('/')[-1]
    if not fname:
        fname = 'file-'.format(str(datetime.datetime.now()).replace(' ', '-'))

    try:
        urllib.urlretrieve(url, fname)
    except IOError:
        return 'Error: Download failed.'

    return 'File {} downloaded.'.format(fname)
