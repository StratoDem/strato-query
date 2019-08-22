"""
StratoDem Analytics : authentication
Principal Author(s) : Michael Clawar
Secondary Author(s) :
Description :

Notes :

August 21, 2019
"""

from typing import Optional

import os

from .exceptions import APITokenNotFoundException

__all__ = ['API_CREDENTIALS', 'authenticate_to_api', 'get_api_token']

KEY_API_TOKEN = 'STRATODEM_API_TOKEN'

API_CREDENTIALS = {KEY_API_TOKEN: None}


def authenticate_to_api(api_token: Optional[str] = None) -> None:
    """
    Authenticate future requests to the StratoDem Analytics API using the API token

    Parameters
    ----------
    api_token: str
        If an argument is passed in, this is used. Otherwise, this looks at the STRATODEM_API_TOKEN
        environment variable for an API token

    Returns
    -------
    """
    if api_token is None:
        api_token = os.environ.get(KEY_API_TOKEN)

        if api_token is None:
            raise APITokenNotFoundException(
                f'Failed to find an API token in the {KEY_API_TOKEN} environment variable')

    API_CREDENTIALS[KEY_API_TOKEN] = api_token


def get_api_token() -> str:
    api_token = API_CREDENTIALS[KEY_API_TOKEN]

    if isinstance(api_token, str):
        return api_token
    else:
        # Try to authenticate first before failing
        authenticate_to_api()

        if isinstance(API_CREDENTIALS[KEY_API_TOKEN], str):
            api_token = API_CREDENTIALS[KEY_API_TOKEN]
            assert isinstance(api_token, str)
            return api_token  # type: str

        raise APITokenNotFoundException(
            'No API authentication set up. '
            'Please use authentication.authenticate_to_api to set up the StratoDem Analytics '
            'API token.')
