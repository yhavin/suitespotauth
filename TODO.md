### 2024-02-26 1:32 pm
Abstractify credential storage and retrieval to separate classes which expose username and password attributes to the main auth class

- Local storage is on keyring, e.g., LocalCredentials
- AWS storage is via SSM, e.g., AWSCredentials
- GCP ...
- Azure ...

```python
credential_source = AWSCredentials(
    username_path="...",
    password_path="..."
)

auth = SuiteSpotAuth(
    credential_source=credential_source
)
```

Error messages and validatiion can happen inside credential source class rather than auth