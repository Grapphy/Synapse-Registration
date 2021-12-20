#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
_utils.py - Utility functions
"""

# Python built-in libraries
import string
import random


def random_string(length: int = 32) -> str:
    return "".join(random.choice(string.ascii_letters) for i in range(length))
