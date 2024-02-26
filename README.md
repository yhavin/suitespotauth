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
If you are running the package locally, your SuiteSpot credentials are securely stored on your computer using (macOS Keychain or Windows Credential Locker). Run the following command to set your SuiteSpot credentials:
```shell
$ suitespotauth-configure
```

### Cloud environment
If you are running the package in a cloud environment, `suitespotauth` can retrieve your SuiteSpot credentials from the cloud provider. Please see the [Cloud configuration](#cloud-configuration) section below before continuing.

## Usage
1. Import the authenticator class:
```python
from suitespotauth.auth import SuiteSpotAuth
```

2. Import your chosen credential storage class:
```python
# Import at least one
from suitespotauth.credentials import (
    LocalCredentialStorage,  # For local environments using `suitespot-configure`
    AWSCredentiaStorage,
    GCPCredentialStorage,
    AzureCredentialStorage
)
```

3. Create a credential storage instance:
```python
# Local storage after running `suitespot-configure`
credential_storage = LocalCredentialStorage()

# AWS storage
credential_storage = AWSCredentialStorage(
    username_path="/path/to/suitespot/username/in/ssm",
    password_path="/path/to/suitespot/password/in/ssm"
)

# GCP storage
credential_storage = GCPCredentialStorage(
    project_id="my-gcp-project-id",
    username_secret_id="suitespot-username-secret-id",
    password_secret_id="suitespot-password-secret-id"
)

# Azure storage
credential_storage = AzureCredentialStorage(
    vault_url="https://my.azure.keyvault.url",
    username_secret_name="suitespot-username-secret-name",
    password_secret_name="suitespot-password-secret-name"
)
```

4. Create an authenticator instance and provide your credential storage instance
```python
auth = SuiteSpotAuth(
    credential_storage=credential_storage,
    api_token_name="Custom SuiteSpot API token name"
)
```

5. Use the `access_token` attribute in your data API request header:
```python
access_token = auth.access_token
"Authorization": f"Bearer {access_token}"
```

Official SuiteSpot data API docs should be retrieved directly from your SuiteSpot representative.

## Cloud configuration
### AWS
`suitespotauth` supports using AWS Systems Manager Parameter Store (SSM) to retrieve SuiteSpot credentials. You must have IAM permissions for your runtime (e.g., Lambda) to access the parameters. Instructions for IAM permissions are beyond the scope of this readme.

Set two SSM parameters, username and password, named anything you want. Choose `SecureString` type when creating the parameters. Then, provide the paths to these parameters when creating the `AWSCredentialStorage` object. See the [Usage](#usage) section above.

### GCP
`suitespotauth` supports using GCP Secret Manager to retrieve SuiteSpot credentials. Set two secrets, username and password, named anything you want. Then, provide the Project ID and the paths to these two secrets when creating the `GCPCredentialStorage` object. See the [Usage](#usage) section above.

### Azure
`suitespotauth` supports using Azure Key Vault to retrieve SuiteSpot credentials. Set two secrets, username and password, named anything you want. Then, provide the Vault URL and the names of these two secrets when creating the `AzureCredentialStorage` object. See the [Usage](#usage) section above.

## Disclaimer
- This is an unofficial package and is not affiliated with SuiteSpot. The official SuiteSpot authentication API docs can be found at: https://auth.suitespot.io/api
- The SuiteSpot authentication API may change at any time, which can cause breaking changes to this package. Please open an issue on GitHub if you notice such problems