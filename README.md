# SuiteSpot Authentication

[![PyPI](https://img.shields.io/pypi/v/suitespotauth?color=blue)](https://pypi.org/project/suitespotauth/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/blog/license/mit)

## Introduction
This package is a light wrapper for the SuiteSpot authentication API to provide easy generation of an access token to be used in SuiteSpot data API calls.

Suitespot data API requests require Bearer Authorization including an access token. This package provides an abstraction layer to easily generate an access token.

## Installation
```shell
$ pip install suitespotauth
```

## Usage
1. Set your SuiteSpot credentials (username and password)
```shell
$ suitespotauth-configure
```

2. In your Python program, import the authenticator class
```python
from suitespotauth import SuiteSpotAuth
```

3. Create a class instance
```python
auth = SuiteSpotAuth()

# Optionally, provide a name variable, which is stored in the SuiteSpot API token object
auth = SuiteSpotAuth("My Company")
```

4. Use the `access_token` attribute in your data API request header
```python
"Authorization": f"Bearer {auth.access_token}"
```

Official SuiteSpot data API docs should be retrieved directly from your SuiteSpot representative.

## Configuration
You must have a SuiteSpot username and password to use this package. When you run `suitespotauth-configure` from the command line, your credentials will be securely stored on your computer using [`keyring`](https://github.com/jaraco/keyring).

## Disclaimer
- This package is unofficial and is not affiliated with SuiteSpot. The official SuiteSpot authentication API docs can be found at: https://auth.suitespot.io/api#/
- The SuiteSpot authentication API may change at any time, which can cause breaking changes to this package. Please open an issue on GitHub if you notice such problems