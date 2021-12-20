#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
setup.py - Installs this repository as a package

Steps:
    For development (In the repo directory):
    >>> pip install -e . 

    For installation (In the repo directory):
    >>> pip install .
"""

__author__ = "Grapphy"

# Python standard libraries
from setuptools import setup


setup(
   name='synapse_registration',
   version='1.0',
   description='Creates accounts on a Synapse server solving captcha and email verification.',
   author='Grapphy',
   packages=['synapse_registration']
)
