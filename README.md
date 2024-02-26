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

## Configuration
This package relies on your SuiteSpot username and password, since SuiteSpot's authentication API uses them in creating Basic Authorization for some requests. The username and password can be securely stored either on your computer or in a cloud environment.

### Local environment
If you are running the package locally, your SuiteSpot credentials are securely stored on your computer using [`keyring`](https://github.com/jaraco/keyring). Run the following command to set your SuiteSpot credentials:
```shell
$ suitespotauth-configure
```

### Cloud environment
If you are running the package in a cloud environment, `suitespotauth` can retrieve your SuiteSpot credentials from the cloud provider. Please see the [Cloud configuration](#cloud-configuration) section below before continuing.

## Usage
1. Import the authenticator class:
```python
from suitespotauth import SuiteSpotAuth
```

2. Create a class instance:
```python
# Basic usage
auth = SuiteSpotAuth()

# Optionally, provide a name which gets stored in the SuiteSpot API token object
auth = SuiteSpotAuth(api_token_name="Custom API token name")

# If using AWS SSM to store SuiteSpot credentials, provide the SSM paths to your username and password parameters
auth = SuiteSpotAuth(
    ssm_username_path="/path/to/suitespot/username/parameter/in/ssm",
    ssm_password_path="/path/to/suitespot/password/parameter/in/ssm"
)
```

3. Use the `access_token` attribute in your data API request header:
```python
access_token = auth.access_token
"Authorization": f"Bearer {access_token}"
```

Official SuiteSpot data API docs should be retrieved directly from your SuiteSpot representative.

## Cloud configuration
### AWS
`suitespotauth` supports using AWS Systems Manager Parameter Store (SSM) to retrieve SuiteSpot credentials. You must have an AWS account, as well as IAM permissions for your runtime (e.g., Lambda) to access the parameters. Instructions for IAM permissions are beyond the scope of this readme.

You must set two SSM parameters, username and password, and they can be named anything you want. Choose `SecureString` type when creating the parameters. Then, you must provide the paths to these parameters when instantiating the `SuiteSpotAuth` object. See the [Usage](#usage) section above.

### GCP
Future support planned...

### Azure
Future support planned...

## Disclaimer
- This is an unofficial package and is not affiliated with SuiteSpot. The official SuiteSpot authentication API docs can be found at: https://auth.suitespot.io/api
- The SuiteSpot authentication API may change at any time, which can cause breaking changes to this package. Please open an issue on GitHub if you notice such problems