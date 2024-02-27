"""
Command line entry point for configuring SuiteSpot credentials.
"""


import getpass

import keyring


SERVICE = "suitespotauth"


def mask_username(username, show_start=1, show_end=6):
    """Utility function to mask saved username."""
    if len(username) > (show_start + show_end):
        return username[:show_start] + "*" * (len(username) - (show_start + show_end)) + username[-show_end:]
    else:
        return username[:show_start] + "*" * (len(username) - show_start)


def main():
    """Prompt and store local SuiteSpot credentials."""
    stored_username = keyring.get_password(SERVICE, "username")
    if stored_username:
        masked_username = mask_username(stored_username, show_start=1, show_end=6)
        username = input(f"SuiteSpot username [{masked_username}]: ") or stored_username
    else:
        username = input("SuiteSpot username: ")

    stored_password = keyring.get_password(SERVICE, "password")
    if stored_password:
        password = getpass.getpass("SuiteSpot password: [Enter to keep current]: ") or stored_password
    else:
        password = getpass.getpass("SuiteSpot password [Input hidden]: ")

    keyring.set_password(SERVICE, "username", username)
    keyring.set_password(SERVICE, "password", password)