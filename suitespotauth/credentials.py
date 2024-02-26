"""
Classes for managing storage and retrieval of SuiteSpot user credentials.
"""


from abc import ABC, abstractmethod

import keyring
import boto3
from botocore.exceptions import ClientError
from google.cloud import secretmanager
from google.api_core.exceptions import GoogleAPICallError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import HttpResponseError

from .configure import SERVICE
from .exceptions import SuiteSpotAuthError


class CredentialStorage(ABC):

    @property
    @abstractmethod
    def username(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass


class LocalCredentialStorage(CredentialStorage):

    @property
    def username(self):
        username = keyring.get_password(SERVICE, "username")
        if username is None:
            raise SuiteSpotAuthError("Local SuiteSpot username not configured. Run `suitespotauth-configure` from the command line.")
        return username
    
    @property
    def password(self):
        password = keyring.get_password(SERVICE, "password")
        if password is None:
            raise SuiteSpotAuthError("Local SuiteSpot password not configured. Run `suitespotauth-configure` from the command line.")
        return password
    

class AWSCredentialStorage(CredentialStorage):
    def __init__(self, *, username_path, password_path):
        if not username_path or not password_path:
            raise SuiteSpotAuthError("SSM paths for username and password must be provided.")
        
        self._username_path = username_path
        self._password_path = password_path
        self._client = boto3.client("ssm")

    @property
    def username(self):
        try:
            response = self._client.get_parameter(Name=self._username_path, WithDecryption=True)
            return response["Parameter"]["Value"]
        except ClientError as e:
            raise SuiteSpotAuthError(f"Failed to retrieve username from SSM: {e}")
        
    @property
    def password(self):
        try:
            response = self._client.get_parameter(Name=self._password_path, WithDecryption=True)
            return response["Parameter"]["Value"]
        except ClientError as e:
            raise SuiteSpotAuthError(f"Failed to retrieve password from AWS SSM: {e}")
        

class GCPCredentialStorage(CredentialStorage):
    def __init__(self, *, project_id, username_secret_id, password_secret_id):
        if not project_id:
            raise SuiteSpotAuthError("GCP project ID must be provided.")
        if not username_secret_id or not password_secret_id:
            raise SuiteSpotAuthError("GCP secret IDs for username and password must be provided.")
        
        self._project_id = project_id
        self._username_secret_id = username_secret_id
        self._password_secret_id = password_secret_id
        self._client = secretmanager.SecretManagerServiceClient()

    def _retrieve_secret(self, secret_id):
        """Retrieve secret from GCP Secret Manager."""
        name = f"projects/{self._project_id}/secrets/{secret_id}/versions/latest"
        try:
            response = self._client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except GoogleAPICallError as e:
            raise SuiteSpotAuthError(f"Failed to retrieve secret {secret_id} from GCP Secret Manager: {e}")
        
    @property
    def username(self):
        return self._retrieve_secret(self._username_secret_id)
    
    @property
    def password(self):
        return self._retrieve_secret(self._password_secret_id)
    

class AzureCredentialStorage(CredentialStorage):
    def __init__(self, *, vault_url, username_secret_name, password_secret_name):
        if not vault_url:
            raise SuiteSpotAuthError("Azure vault URL must be provided.")
        if not username_secret_name or not password_secret_name:
            raise SuiteSpotAuthError("Azure secret names for username and password must be provided.")
        
        self._vault_url = vault_url
        self._username_secret_name = username_secret_name
        self._password_secret_name = password_secret_name
        self._credential = DefaultAzureCredential()
        self._client = SecretClient(vault_url=self._vault_url, credential=self._credential)

    @property
    def username(self):
        try:
            response = self._client.get_secret(self._username_secret_name)
            return response.value
        except HttpResponseError as e:
            raise SuiteSpotAuthError(f"Failed to retrieve username from Azure: {e}")
        
    @property
    def password(self):
        try:
            response = self._client.get_secret(self._password_secret_name)
            return response.value
        except HttpResponseError as e:
            raise SuiteSpotAuthError(f"Failed to retrieve password from Azure: {e}")