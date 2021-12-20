#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
_request.py - Headers and payloads for
requests. This file shouldn't be modified.
"""

__author__ = "Grapphy"

# Python libraries
from json import dumps
from collections import OrderedDict
from urllib3 import disable_warnings
from requests.sessions import Session
from urllib3.exceptions import InsecureRequestWarning

# Global variables
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/92.0.4515.131 Safari/537.36"
)


class Headers:
    """Headers class contains multiple
    static methods for creating ordered headers
    in order to mimic normal browser behaviour.
    """

    @staticmethod
    def get_default_headers() -> OrderedDict:
        """Default headers"""
        return OrderedDict(
            (
                ("Host", None),
                ("User-Agent", USER_AGENT),
                ("Accept", "*/*"),
                ("Accept-Language", "en-US;q=0.5,en;q=0.3"),
                ("Accept-Encoding", "gzip, deflate"),
            )
        )

    @staticmethod
    def post_matrix_headers(origin: str) -> OrderedDict:
        """Matrix headers for sending POST requests which
        requires an Origin header for resources security.

        Args:
            origin (str): An Origin URL string.

        Returns:
            OrderedDict: Dict containing headers.
        """
        return OrderedDict(
            (
                ("Host", None),
                ("User-Agent", USER_AGENT),
                ("Accept", "application/json"),
                ("Accept-Language", "en-US;q=0.5,en;q=0.3"),
                ("Accept-Encoding", "gzip, deflate"),
                ("Content-Type", "application/json"),
                ("Content-Length", ""),
                ("Origin", origin),
            )
        )


class Payloads:
    """Payloads class contains multiple static
    methods for creating JSON data that is being sent
    through API calls to Synapse (Matrix Backend).
    """

    @staticmethod
    def init_registration(username: str, password: str) -> str:
        return dumps(
            {
                "auth": {},
                "username": username,
                "password": password,
                "inhibit_login": False,
            },
            separators=(",", ":"),
        )

    @staticmethod
    def submit_captcha(
        session: str, username: str, password: str, captcha: str
    ) -> str:
        return dumps(
            {
                "auth": {
                    "session": session,
                    "type": "m.login.recaptcha",
                    "response": captcha,
                },
                "username": username,
                "password": password,
                "inhibit_login": False,
            },
            separators=(",", ":"),
        )

    @staticmethod
    def submit_consent(session: str, username: str, password: str) -> str:
        return dumps(
            {
                "auth": {"session": session, "type": "m.login.terms"},
                "username": username,
                "password": password,
                "inhibit_login": False,
            },
            separators=(",", ":"),
        )

    @staticmethod
    def submit_email(email: str, client_secret: str) -> str:
        return dumps(
            {"email": email, "client_secret": client_secret, "send_attempt": 1}
        )

    @staticmethod
    def submit_threepid(
        session: str,
        username: str,
        password: str,
        sid: str,
        client_secret: str,
    ) -> str:
        return dumps(
            {
                "auth": {
                    "session": session,
                    "type": "m.login.email.identity",
                    "threepid_creds": {
                        "sid": sid,
                        "client_secret": client_secret,
                    },
                    "threepidCreds": {
                        "sid": sid,
                        "client_secret": client_secret,
                    },
                },
                "username": username,
                "password": password,
                "inhibit_login": False,
            }
        )

    @staticmethod
    def create_account(session: str, username: str, password: str) -> str:
        return dumps(
            {
                "auth": {"session": session, "type": "m.login.dummy"},
                "username": username,
                "password": password,
                "inhibit_login": False,
            },
            separators=(",", ":"),
        )


class ISession(Session):
    """ISession is a request.Session interface for
    easily switching to local and external proxies
    and logging request history.

    Attributes:
        proxy (str): A proxy string (default is None)
    """

    def __init__(self, proxy: str = None):
        super().__init__()

        if not proxy:
            self.proxies = None
        else:
            self.proxies = {
                "http": f"http://{proxy}",
                "https": f"https://{proxy}",
            }

        if proxy == "127.0.0.1:8080":
            self.verify = False
            disable_warnings(InsecureRequestWarning)
