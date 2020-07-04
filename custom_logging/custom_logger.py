#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
# Project: logging
# FilePath: /custom_logger.py
# File: custom_logger.py
# Created Date: Saturday, June 27th 2020, 3:19:43 pm
# Author: Craig Bojko (craig@pixelventures.co.uk)
# -----
# Last Modified: Sat Jul 04 2020
# Modified By: Craig Bojko
# -----
# Copyright (c) 2020 Pixel Ventures Ltd.
# ------------------------------------
# <<licensetext>>
"""

import logging
import json
from termcolor import colored

FORMAT = "%(asctime)-15s: %(message)s"
LONG_FORMAT = "%(asctime)-15s %(clientIp)s %(user)-8s %(message)s"
LOG_EXTRA = {"clientIp": "...", "user": "..."}

logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%H:%M:%S")


def format_logger(logger):
    """
    Splits logging call based on type and returns as dict
    """
    def info(log_str):
        logger.info(log_str, extra=LOG_EXTRA)

    def debug(log_str):
        logger.debug(
            log_str, extra=LOG_EXTRA,
        )

    def warning(log_str):
        logger.warning(
            log_str, extra=LOG_EXTRA,
        )

    def error(log_str):
        logger.error(
            log_str, extra=LOG_EXTRA,
        )

    options = {"info": info, "debug": debug, "warning": warning, "error": error}
    return options


def build_log_string(*args, msg="", colors=True):
    """
    Builds a string from message and any extra objects passed in.
    Uses JSON to stringify the additional objects
    """
    items = []

    if isinstance(msg, str) is not True:
        items.append(json.dumps(msg))
    else:
        if msg == "":
            try:
                item = args[0]
            except IndexError:
                return ""
        else:
            items.append(msg)

    if args is not None and len(args) > 0:
        for arg in args:
            i = json.dumps(arg)
            item = i if colors is False else colored(i, "cyan")
            items.append(item)
    log_str = ("\n\t\t").join(items)
    return log_str


def create_logger(level=logging.DEBUG, colors=True):
    """
    Function creates a new logging object and returns
    """
    logger = logging.getLogger()
    logger_handler = logger.handlers[0]  # logging.StreamHandler()

    formatter = logging.Formatter(LONG_FORMAT)
    formatter.datefmt = "%H:%M:%S"
    logger_handler.setFormatter(formatter)

    logger.addHandler(logger_handler)
    logger.setLevel(level)

    console = format_logger(logger)
    return lambda msg="", *args, level="info": console[level](
        build_log_string(msg=msg, colors=colors, *args)
    )


def log(*args, msg="", level="info"):
    """
    Simple log function that will output based on default parameters
    """
    console = create_logger(level=logging.INFO, colors=True)
    console(msg=msg, level=level, *args)
