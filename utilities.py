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


def setup_logging(logname):
    """function to setup basic logging"""
    log = logging.getLogger(logname)
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - line %(lineno)d - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log