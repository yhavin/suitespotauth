"""
Class for retrieving access token to make API calls to SuiteSpot analytics.
"""


import base64

import requests

from .exceptions import SuiteSpotAuthError
from .credentials import CredentialStorage


class SuiteSpotAuth:
    BASE_URL = "https://auth.suitespot.io/api/api-tokens"

    def __init__(self, *, credential_storage: CredentialStorage, api_token_name="SuiteSpot User"):
        if not isinstance(credential_storage, CredentialStorage):
            raise TypeError("`credential_storage` must be an sub-instance of CredentialStorage.")
        
        self._credential_storage = credential_storage
        self._api_token_name = api_token_name
        self._basic_auth_headers = self._generate_basic_auth_headers()
        self._api_token = None
        self._access_token = None
        self._authenticate()

    def _generate_basic_auth_headers(self): 
        """Generate Basic Authorization header for API token requests."""
        basic_auth_string = base64.b64encode(f"{self._credential_storage.username}:{self._credential_storage.password}".encode()).decode()
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