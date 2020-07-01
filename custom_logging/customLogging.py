#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project: logging
# FilePath: /customLogging.py
# File: customLogging.py
# Created Date: Saturday, June 27th 2020, 3:19:43 pm
# Author: Craig Bojko (craig@pixelventures.co.uk)
# -----
# Last Modified: Wed Jul 01 2020
# Modified By: Craig Bojko
# -----
# Copyright (c) 2020 Pixel Ventures Ltd.
# ------------------------------------
# <<licensetext>>
###

import logging
import json
from termcolor import colored

FORMAT = "%(asctime)-15s: %(message)s"
LONG_FORMAT = '%(asctime)-15s %(clientIp)s %(user)-8s %(message)s'
LOG_EXTRA = { 'clientIp': '...', 'user': '...' }

logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    datefmt="%H:%M:%S"
)

def formatLogger(logger):
  def info(logStr): logger.info(logStr, extra=LOG_EXTRA)
  def debug(logStr): logger.debug(logStr, extra=LOG_EXTRA,)
  def warning(logStr): logger.warning(logStr, extra=LOG_EXTRA,)
  def error(logStr): logger.error(logStr, extra=LOG_EXTRA,)
  options = {
    'info': info,
    'debug': debug,
    'warning': warning,
    'error': error
  }
  return options


def buildLogString(msg='', *args, colors=True):
  items = []
  items.append(msg)
  if args is not None and len(args) > 0:
    for arg in args:
      i = json.dumps(arg)
      item = i if colors == False else colored(i, 'cyan')
      items.append(item)
  logStr = ("\n\t\t").join(items)
  return logStr


def createLogger(level=logging.DEBUG, colors=True):
  logger = logging.getLogger()
  logger_handler = logger.handlers[0] # logging.StreamHandler()
  
  formatter = logging.Formatter(LONG_FORMAT)
  formatter.datefmt = "%H:%M:%S"
  logger_handler.setFormatter(formatter)

  logger.addHandler(logger_handler)
  logger.setLevel(level)

  console = formatLogger(logger)
  return lambda msg='', *args, type='info': console[type](buildLogString(msg, *args, colors=colors))


def log(msg='', *args, type='info'):
  console = createLogger(level=logging.INFO, colors=True)
  console(msg, *args, type=type)
