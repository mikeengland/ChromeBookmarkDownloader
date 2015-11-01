# -*- coding: utf-8 -*-

import os
import sys
import errno
import logging


def mkdir_p(path):
    """function to recursively create directories (like mkdir -p)"""
    # taken from http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
            raise