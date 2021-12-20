#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
verification.py - Verifies emails.
"""

# Python libraries
from json import loads
from time import sleep
from bs4 import BeautifulSoup
from requests.sessions import Session
from requests.exceptions import RequestException


class TemporaryInbox(Session):
    BASE = "https://www.fakemail.net"

    def __init__(self, timeout: int = 120):
        super().__init__()
        self.headers = {"X-Requested-With": "XMLHttpRequest"}

        self.timeout = timeout
        self.email = self.get_email()

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<Email={self.email}>"

    def get_email(self) -> str:
        url = f"{self.BASE}/index/index"
        with self.get(url) as response:
            try:
                r_text = response.text[1:]
                r_json = loads(r_text)
                return r_json["email"]
            except KeyError:
                raise TypeError("Couldnt get email")

    def get_inbox(self) -> str:
        url = f"{self.BASE}/email/id/2"
        counter = self.timeout // 10

        for _ in range(counter):
            try:
                response = self.get(url)
                r_text = response.text[1:]
                if not "There was en error" in r_text:
                    return r_text
            except RequestException:
                # Fakemail.net is the service used for verification
                # and it might not be stable in some cases.
                pass
            except BaseException as e:
                raise e

            sleep(10)
        raise TimeoutError("Timeout error for TempInbox")

    @staticmethod
    def get_matrix_link(mail_html: str) -> str:
        parser = BeautifulSoup(mail_html, "lxml")
        return parser.select("a")[0].get("href")
