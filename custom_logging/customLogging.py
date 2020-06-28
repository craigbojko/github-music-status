#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project: logging
# FilePath: /customLogging.py
# File: customLogging.py
# Created Date: Saturday, June 27th 2020, 3:19:43 pm
# Author: Craig Bojko (craig@pixelventures.co.uk)
# -----
# Last Modified: Sat Jun 27 2020
# Modified By: Craig Bojko
# -----
# Copyright (c) 2020 Pixel Ventures Ltd.
# ------------------------------------
# <<licensetext>>
###

import logging
from termcolor import colored

FORMAT = "%(asctime)-15s: %(message)s"
LONG_FORMAT = '%(asctime)-15s %(clientIp)s %(user)-8s %(message)s'
LOG_EXTRA = { 'clientIp': '...', 'user': '...' }
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    datefmt="%H:%M:%S"
)
console = logging.getLogger('console')
console_handler = logging.StreamHandler()
console_handler.setFormatter(FORMAT)

def log(msg='', *args, type='info'):
    items = []
    items.append(msg)
    for arg in args:
        items.append(colored(arg, 'cyan'))
    logStr = ("\n\t\t").join(items)

    formatter = logging.Formatter(LONG_FORMAT)
    formatter.datefmt = "%H:%M:%S"
    console_handler.setFormatter(formatter)

    def info(): console.info(logStr, extra=LOG_EXTRA)
    def debug(): console.debug(logStr, extra=LOG_EXTRA,)
    def warning(): console.warning(logStr, extra=LOG_EXTRA,)
    def error(): console.error(logStr, extra=LOG_EXTRA,)

    options = {
        'info': info,
        'debug': debug,
        'warning': warning,
        'error': error
    }
    options[type]()

