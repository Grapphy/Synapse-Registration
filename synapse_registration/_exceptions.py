#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_exceptions.py - This module contains exception classes to
easily identify errors at runtime
"""

__author__ = "Grapphy"


class DefaultException(IOError):
    def __init__(self, *args, **kwargs):
        error = kwargs.pop("error")
        msg = kwargs.pop("msg")

        if all([error, msg]):
            self.error = error
            self.message = msg

        super(DefaultException, self).__init__(msg)


class SynapseException(DefaultException):
    """An error related to Riot/Matrix API was raised"""

    def __init__(self, json: dict):
        error = json["errcode"]
        msg = json["error"]

        super(SynapseException, self).__init__(error=error, msg=msg)


class ServerException(DefaultException):
    """An error related to the home server configuration"""

    def __init__(self, err_msg: str):
        error = "Server Exception"
        msg = err_msg

        super(ServerException, self).__init__(error=error, msg=msg)
