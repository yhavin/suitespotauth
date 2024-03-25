# SuiteSpot Authentication

[![PyPI](https://img.shields.io/pypi/v/suitespotauth?color=blue&label=pypi)](https://pypi.org/project/suitespotauth/)
[![Downloads](https://img.shields.io/pepy/dt/suitespotauth?color=purple&label=downloads)](https://pypistats.org/packages/suitespotauth)
[![License](https://img.shields.io/badge/License-MIT-green.svg?color=dark-green&label=license)](https://opensource.org/blog/license/mit)

## Introduction
This package is a light wrapper for the SuiteSpot authentication API to provide easy creation of an access token. This token is required as part of Bearer Authorization in all calls to SuiteSpot's analytics API.

## Installation
```shell
$ pip install suitespotauth
```
or
```shell
$ python -m pip install suitespotauth
```

## Configuration
This package relies on your SuiteSpot username and password, since SuiteSpot's authentication API uses them in creating Basic Authorization for the initial authentication flow request. The username and password can be securely stored either on your computer or in a cloud provider.

### Local environment
If you are running the package locally, you can store your SuiteSpot credentials on your computer (macOS Keychain or Windows Credential Locker). This is built on top of [keyring](https://github.com/jaraco/keyring). 

Run the following command to set your local SuiteSpot credentials:
```shell
$ suitespotauth-configure
```

### Cloud environment
You can also store your SuiteSpot credentials in a cloud provider secret manager. This helps for cloud environments (e.g., Lambda) where you can't use local secret storage. (Of course, you may choose to store your SuiteSpot credentials in a cloud provider even if you are running locally.) 

See the [Cloud configuration](#cloud-configuration) section for the syntax used for cloud credential storage.

## Usage
```python
from suitespotauth import SuiteSpotAuth
from suitespotauth import LocalCredentialStorage  # Or a cloud option

my_credentials = LocalCredentialStorage()

auth = SuiteSpotAuth(
    credential_storage=my_credentials,
    api_token_name="Custom SuiteSpot API token name"  # Optional
)

access_token = auth.access_token

headers = {
    "Authorization": f"Bearer {access_token}"
}
```

## Cloud configuration
### AWS
`suitespotauth` supports using AWS Parameter Store (SSM) to retrieve SuiteSpot credentials. You must have IAM permissions for your runtime (e.g., Lambda) to access the parameters. Instructions for IAM permissions are beyond the scope of this readme.

Set two SSM parameters, username and password, named anything you want. Choose `SecureString` type when creating the parameters. Then, provide the paths to these parameters when creating the `AWSCredentialStorage` object.

Install the AWS dependencies:
```shell
$ pip install 'suitespotauth[aws]'
```

```python
from suitespotauth import AWSCredentialStorage

my_credentials = AWSCredentialStorage(
    username_path="/path/to/suitespot/username/in/ssm",
    password_path="/path/to/suitespot/password/in/ssm"
)
```

### GCP
`suitespotauth` supports using GCP Secret Manager to retrieve SuiteSpot credentials. Set two secrets, username and password, named anything you want. Then, provide the Project ID and the paths to these two secrets when creating the `GCPCredentialStorage` object. 

Install the GCP dependencies:
```shell
$ pip install 'suitespotauth[gcp]'
```

```python
from suitespotauth import GCPCredentialStorage

my_credentials = GCPCredentialStorage(
    project_id="my-gcp-project-id",
    username_secret_id="suitespot-username-secret-id",
    password_secret_id="suitespot-password-secret-id"
)
```

### Azure
`suitespotauth` supports using Azure Key Vault to retrieve SuiteSpot credentials. Set two secrets, username and password, named anything you want. Then, provide the Vault URL and the names of these two secrets when creating the `AzureCredentialStorage` object. 

Install the Azure dependencies:
```shell
$ pip install 'suitespotauth[azure]'
```

```python
from suitespotauth import AzureCredentialStorage

my_credentials = AzureCredentialStorage(
    vault_url="https://my.azure.keyvault.url",
    username_secret_name="suitespot-username-secret-name",
    password_secret_name="suitespot-password-secret-name"
)
```

## Disclaimer
- This is an unofficial package and is not affiliated with SuiteSpot. The official SuiteSpot authentication API docs can be found at: https://auth.suitespot.io/api
- The SuiteSpot authentication API may change at any time, which can cause breaking changes to this package. Please open an issue on GitHub if you notice such problems