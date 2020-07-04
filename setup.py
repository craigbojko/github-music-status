#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project: github-music-status
# FilePath: /setup.py
# File: setup.py
# Created Date: Sunday, June 28th 2020, 10:20:19 pm
# Author: Craig Bojko (craig@pixelventures.co.uk)
# -----
# Last Modified: Sat Jul 04 2020
# Modified By: Craig Bojko
# -----
# Copyright (c) 2020 Pixel Ventures Ltd.
# ------------------------------------
# <<licensetext>>
###

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='github-music-status',
    version='1.0.0',
    description='',
    long_description=readme,
    author='Pixel Ventures Ltd.',
    author_email='craig@pixelventures.co.uk',
    url='https://github.com/pixelventures/github-music-status',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        "termcolor",
        "pytest",
        "pylint"
    ]
)