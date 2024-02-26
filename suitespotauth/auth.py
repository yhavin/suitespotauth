"""
Class for retrieving access token to make API calls to SuiteSpot.
"""


import base64

import requests
import keyring
import boto3
from botocore.exceptions import ClientError

from suitespotauth.configure import SERVICE


class SuiteSpotAuthError(Exception):
    """Custom exception class for SuiteSpotAuth errors."""
    pass


class SuiteSpotAuth:
    BASE_URL = "https://auth.suitespot.io/api/api-tokens"

    def __init__(self, *, api_token_name="SuiteSpot User", ssm_username_path=None, ssm_password_path=None):
        self._api_token_name = api_token_name
        self._ssm_username_path = ssm_username_path
        self._ssm_password_path = ssm_password_path
        self._credentials = self._ensure_credentials()
        self._basic_auth_headers = self._generate_basic_auth_headers()
        self._api_token = None
        self._access_token = None
        self._authenticate()

    def _fetch_credentials_from_ssm(self, path):
        """Retrieve credentials from AWS Parameter Store (SSM)."""
        ssm = boto3.client("ssm")
        try:
            parameter = ssm.get_parameter(Name=path, WithDecryption=True)["Parameter"]["Value"]
            return parameter
        except ClientError as e:
            raise SuiteSpotAuthError(f"An error occurred trying to fetch parameters in SSM from path '{path}'.\n{e}")

    def _ensure_credentials(self):
        """Check if SuiteSpot credentials have been entered or fetch from AWS Parameter Store."""
        credentials = {}
        
        if bool(self._ssm_username_path) != bool(self._ssm_password_path):
            raise SuiteSpotAuthError("SSM paths for both username and password must be provided.")
        
        if self._ssm_username_path and self._ssm_password_path:
            credentials["username"] = self._fetch_credentials_from_ssm(self._ssm_username_path)
            credentials["password"] = self._fetch_credentials_from_ssm(self._ssm_password_path)
        else:
            for credential in ["username", "password"]:
                stored_value = keyring.get_password(SERVICE, credential)
                if not stored_value:
                    raise SuiteSpotAuthError("SuiteSpot credentials not configured. Run 'suitespotauth-configure'.")
                credentials[credential] = stored_value
        
        return credentials

    def _generate_basic_auth_headers(self): 
        """Generate Basic Authorization header for API token requests."""
        basic_auth_string = base64.b64encode(f"{self._credentials["username"]}:{self._credentials["password"]}".encode()).decode()
        basic_auth_headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {basic_auth_string}",
            "Content-Type": "application/json"
        }
        return basic_auth_headers
    
    def _api_token_exists(self):
        """Check if an API token already exists."""
        response = requests.get(SuiteSpotAuth.BASE_URL, headers=self._basic_auth_headers)

        if response.status_code == 200:
            if response.json().get("apiTokens")[0]:
                self._api_token = response.json().get("apiTokens")[0]["apiTokenId"]
                return True
        return False
    
    def _create_api_token(self):
        """Create an API token if none exists."""
        body = {
            "name": self._api_token_name,
            "expiryTTL": "1w",
            "version": 3
        }
        response = requests.post(SuiteSpotAuth.BASE_URL, headers=self._basic_auth_headers, json=body)

        if response.status_code == 201:
            self._api_token = response.json().get("apiTokenId")
        else:
            raise SuiteSpotAuthError(f"API token creation request failed: {response.status_code}\n{response.json()}")
        
    def _exchange_api_token_for_access_token(self):
        """Exchange an API token for an access token."""
        url = f"{SuiteSpotAuth.BASE_URL}/{self._api_token}/new-access-token"
        response = requests.post(url, headers=self._basic_auth_headers)

        if response.status_code == 201:
            self._access_token = response.json().get("accessToken")
        else:
            raise SuiteSpotAuthError(f"Access token exchange request failed: {response.status_code}\n{response.json()}")
        
    def _authenticate(self):
        """Wrapper method for orchestration of authorization flow."""
        if not self._api_token_exists():
            self._create_api_token()
        self._exchange_api_token_for_access_token()

    @property
    def access_token(self):
        """Property to retrieve access token."""
        if not self._access_token:
            self._authenticate()
        return self._access_token