#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
captcha.py - Solves google recaptcha
using external api.
"""

__author__ = "Grapphy"

# Built-in libraries
import time
from requests.api import get


class CaptchaService:
    t_in = "https://2captcha.com/in.php"
    t_res = "https://2captcha.com/res.php"

    def __init__(self, key: str):
        self.key = key

    def solve(self, site_key: str, url: str, timeout: int = 120) -> str:
        params = dict(
            key=self.key,
            method="userrecaptcha",
            googlekey=site_key,
            pageurl=url,
            json=1,
        )

        with get(self.t_in, params=params) as res:
            res_json = res.json()

            if not res_json["status"]:
                raise Exception(res_json["request"])
            req_id = res_json["request"]

        params = dict(key=self.key, action="get", id=req_id, json=1)

        counter = timeout // 5
        for _ in range(counter):
            with get(self.t_res, params=params) as res:
                res_json = res.json()

                if res_json["status"]:
                    return res_json["request"]
                if (
                    not res_json["status"]
                    and res_json["request"] != "CAPCHA_NOT_READY"
                ):
                    raise Exception(res_json["request"])

                time.sleep(5)

        raise Exception("Timeout for captcha solution.")
