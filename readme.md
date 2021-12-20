# Synapse Registration
This repository contains a script for creating an account at Synapse, which is Matrix.org backend for room and users management. Using this piece of code will allow you to make new accounts on any given homeserver with support for captcha and email verification.

Currently it uses a captcha solving service for those homeservers that requires them and a module for verifying emails. Again this depends on the homeserver.

## Table of contents
* [Example with no verifications](https://github.com/grapphy/Synapse-Registration#example-with-no-verifications)
* [Example with Google Recaptcha](https://github.com/grapphy/Synapse-Registration#example-with-google-recaptcha)
* [Example with Recaptcha and email verification](https://github.com/grapphy/Synapse-Registration#example-with-recaptcha-and-email-verification)
* [Using proxies](https://github.com/grapphy/Synapse-Registration#using-proxies)
* [Requirements](https://github.com/grapphy/Synapse-Registration#requirements)
* [Credits](https://github.com/grapphy/Synapse-Registration#credits)

## Example with no verifications
```python
# Importing function from module.
from synapse_registration import create_synapse_account

# Homeserver and account credentials.
homeserver = "any_homeserver.net"
username = "example-test-acc"
password = "aNyRandomPassWd"

# Results from function.
account_data: dict
account_data = create_synapse_account(homeserver, username, password)

# 'access_token' key should contain Authorization token.
assert account_data.get("access_token")
```

## Example with Google recaptcha
```python
# Importing function and class from module.
from synapse_registration import create_synapse_account
from synapse_registration.captcha import CaptchaService

# Homeserver, account credentials and captcha service.
homeserver = "any_homeserver.net"
username = "example-test-acc"
password = "aNyRandomPassWd"

# Currently it uses a credit-type service for captcha solving
# Requires you to have a valid key.
captcha = CaptchaService("SECRET-CLIENT-KEY")

# Results from function.
account_data: dict
account_data = create_synapse_account(homeserver, username, password, captcha)

# 'access_token' key should contain Authorization token.
assert account_data.get("access_token")
```

## Example with recaptcha and email verification (Matrix.org)
```python
# Importing function and classes from module.
from synapse_registration import create_synapse_account
from synapse_registration.captcha import CaptchaService
from synapse_registration.verification import TemporaryInbox

# Homeserver, account credentials and captcha service.
homeserver = "any_homeserver.net"
username = "example-test-acc"
password = "aNyRandomPassWd"

# Currently it uses a credit-type service for captcha solving
# Requires you to have a valid key.
captcha = CaptchaService("SECRET-CLIENT-KEY")

# Temporary email inbox for verification
tempin = TemporaryInbox(timeout=25)

# Results from function.
account_data: dict
account_data = create_synapse_account(
    homeserver, username, password, captcha, tempin
)

# 'access_token' key should contain Authorization token.
assert account_data.get("access_token")
```

## Using proxies
Any proxy can be given in the format of `user:pass@host:port` or just `host:port` when calling `create_synapse_account`

```python
proxy = "username:password@host:port"
account_data = create_synapse_account(
    homeserver, username, password, proxy=proxy
)
```

## Requirements
```console
beautifulsoup4==4.10.0
requests==2.26.0
urllib3==1.23
```

## Credits
Created and maintained by [@Grapphy](https://github.com/grapphy). Feel free to contribute to this repo in any form.