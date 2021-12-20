#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
registration.py - Creates an account
at any Matrix instance.
"""

__author__ = "Grapphy"

# Python libraries
from . import _request
from . import _exceptions
from . import _utils
from urllib.parse import urljoin

# Global variables
_REGISTRATION = "/_matrix/client/r0/register"


def lookup_synapse_host(session: _request.ISession, home_server: str) -> str:
    """Lookup for homeserver base url where Synapse is hosted.

    Args:
        session (_request.ISession): A request session.
        home_server (str): A home_server domain string.

    Returns:
        str: URL string where Synapse handles API calls

    Raises:
        ServerException: Server is misconfigured and doesn't
          return a proper well-known result or it is missing.
    """
    session.headers = _request.Headers.get_default_headers()
    well_known = f"{home_server}/.well-known/matrix/client"

    with session.get(well_known) as res:
        if res.status_code != 200:
            raise _exceptions.ServerException(
                f"No /.well-known/ found at {home_server}"
            )

        r_json = res.json()

        try:
            return r_json["m.homeserver"]["base_url"]
        except KeyError:
            raise _exceptions.ServerException(
                f"Invalid /.well-knon/ at {home_server}"
            )


def create_synapse_account(
    home_server: str,
    username: str,
    password: str,
    captcha: object = None,
    tempin: object = None,
    proxy: str = None,
) -> dict:
    """Creates an account at synapse (Matrix backend). Currently it
    does not handle servers that need captcha solving or email
    verification.

    Args:
        home_server (str): The homeserver where Matrix is hosted.
        username (str): Username of the account to create.
        password (str): Password for the account to create.
        captcha (captcha.CaptchaService): A CaptchaService instance
          for Google Recaptcha solving (default is None).
        proxy (str): Any proxy to use (default is None).

    Returns:
        dict: a dict with account data.

    Raises:
        SynapseException: Some error related to Matrix Backend.
        BaseException: Something not implemented.
    """
    if not home_server.startswith("http"):
        home_server = f"https://{home_server}"

    with _request.ISession(proxy) as session:
        synapse_host = lookup_synapse_host(session, home_server)
        session.headers = _request.Headers.post_matrix_headers(home_server)
        registration_endpoint = urljoin(synapse_host, _REGISTRATION)

        _data = _request.Payloads.init_registration(username, password)
        with session.post(registration_endpoint, data=_data) as res:
            r_json = res.json()

            if "error" in r_json:
                raise _exceptions.SynapseException(r_json)

            sess_key = r_json["session"]

            if "m.login.recaptcha" in r_json["params"]:
                if not captcha:
                    raise Exception("Captcha is required in this homeserver")

                site_key = r_json["params"]["m.login.recaptcha"]["public_key"]
                solution = captcha.solve(site_key, registration_endpoint)
                _data = _request.Payloads.submit_captcha(
                    sess_key, username, password, solution
                )
                session.post(registration_endpoint, data=_data)

            if "m.login.email.identity" in r_json["flows"][0]["stages"]:
                if not tempin:
                    raise Exception(
                        "Email verification is required in this homeserver"
                    )

                client_secret = _utils.random_string()

                _data = _request.Payloads.submit_email(
                    str(tempin), client_secret
                )
                e_url = f"{registration_endpoint}/email/requestToken"
                with session.post(e_url, data=_data) as res:
                    r_json = res.json()

                    if ("error") in r_json:
                        raise _exceptions.SynapseException(r_json)

                    sid = r_json["sid"]

                mail = tempin.get_inbox()
                v_url = tempin.get_matrix_link(mail)

                session.headers = _request.Headers.get_default_headers()
                with session.get(v_url) as res:
                    if not "validated" in res.text:
                        raise _exceptions.ServerException(res.text)

                _data = _request.Payloads.submit_threepid(
                    sess_key, username, password, sid, client_secret
                )
                session.headers = _request.Headers.post_matrix_headers(
                    home_server
                )
                with session.post(registration_endpoint, data=_data) as res:
                    r_json = res.json()

                    if "m.login.email.identity" not in r_json["completed"]:
                        raise Exception("Couldn't verify email")

            if "m.login.terms" in r_json["flows"][0]["stages"]:
                _data = _request.Payloads.submit_consent(
                    sess_key, username, password
                )
                session.post(registration_endpoint, data=_data)

        _data = _request.Payloads.create_account(sess_key, username, password)
        with session.post(registration_endpoint, data=_data) as res:
            r_json = res.json()

            if ("error" in r_json) or ("access_token" not in r_json):
                raise _exceptions.SynapseException(r_json)

            return r_json
