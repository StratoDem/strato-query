"""
StratoDem Analytics : api_query
Principal Author(s) : Eric Linden, Michael Clawar
Secondary Author(s) :
Description :

Notes :

August 21, 2019
"""

import time

from typing import Dict, Optional, Union

import requests

import pandas

from strato_query import constants as cc
from .query_structures import *
from .authentication import get_api_token
from .exceptions import APIQueryFailedException

__all__ = ['SDAPIQuery']

T_DF = pandas.DataFrame


class SDAPIQuery:
    @classmethod
    def submit_query(cls,
                     query_params: Optional[APIQueryParams] = None,
                     queries_params: Optional[Dict[str, APIQueryParams]] = None,
                     timeout: Optional[float] = 60.0,
                     headers: Optional[Dict[str, str]] = None) -> Union[T_DF, Dict[str, T_DF]]:
        """
        Determines the proper method to use and passes values along for request submission

        Parameters
        ----------
        query_params: Optional[APIQueryParams] = None
            A single query params object to submit as part of the request
        queries_params: Optional[Dict[str, APIQueryParams]] = None
            A list of dicts, with query params as the values, to be submitted together
        timeout: Optional[float]=60.0
            The time allowed before a request times out, where 1 second is 1.0
        headers: Optional[Dict[str, str]] = None
            Optional request headers
        Returns
        -------
        The result from the request, either a pandas dataframe or a dict with dataframes as values
        """
        assert query_params is None or isinstance(query_params, APIQueryParams)
        assert queries_params is None or isinstance(queries_params, dict)
        if queries_params is not None:
            assert all(isinstance(query, APIQueryParams) for query in queries_params.values())
        assert not (query_params is None and queries_params is None)
        assert not (query_params is not None and queries_params is not None)

        if query_params is not None:
            return cls.query_api_df(query_params=query_params, headers=headers, timeout=timeout)
        elif queries_params is not None:
            return cls.query_api_multiple(queries=queries_params, headers=headers, timeout=timeout)

    @staticmethod
    def query_api_json(query_params: APIQueryParams,
                       timeout: Optional[float] = 60.0,
                       headers: Optional[Dict[str, str]] = None) -> dict:
        """
        Submits the query params and returns the resulting data
        Parameters
        ----------
        query_params: APIQueryParams
            The query params to be used in the POST request
        timeout: Optional[float]=60.0
            The time allowed before a request times out, where 1 second is 1.0
        headers: Optional[Dict[str, str]] = None
            Optional request headers

        Returns
        -------
        A dict containing the query result
        """
        json_data = _submit_post_request(
            json_dict=dict(token=get_api_token(), query=query_params.to_api_struct()),
            headers=headers,
            timeout=timeout)

        return json_data['data'][0]

    @staticmethod
    def query_api_df(query_params: APIQueryParams,
                     timeout: Optional[float] = 60.0,
                     headers: Optional[Dict[str, str]] = None) -> pandas.DataFrame:
        """
        Submits the query params and returns the resulting data

        Parameters
        ----------
        query_params: APIQueryParams
            The query params to be used in the POST request
        timeout: Optional[float]=60.0
            The time allowed before a request times out, where 1 second is 1.0
        headers: Optional[Dict[str, str]] = None
            Optional request headers

        Returns
        -------
        A pandas dataframe containing the query result
        """
        json_data = _submit_post_request(
            json_dict=dict(token=get_api_token(), query=query_params.to_api_struct()),
            headers=headers,
            timeout=timeout)

        df_ = pandas.DataFrame(json_data['data'])
        df_.columns = [c.upper() for c in df_.columns]

        return df_

    @staticmethod
    def query_api_multiple(queries: Dict[str, APIQueryParams],
                           timeout: Optional[float] = 60.0,
                           chunksize: int = 500,
                           headers: Optional[Dict[str, str]] = None) -> Dict[str, pandas.DataFrame]:
        """
        Submits the query params and returns the resulting data

        Parameters
        ----------
        queries: Dict[str, APIQueryParams]
            The query params to be used in the POST request
        timeout: Optional[float]=60.0
            The time allowed before a request times out, where 1 second is 1.0
        chunksize: int=500
            The maximum size of chunks submitted to the API service at once
        headers: Optional[Dict[str, str]] = None
            Optional request headers

        Returns
        -------
        A dict with pandas dataframes as the values for each of the query params in the input dict
        """
        assert isinstance(chunksize, int) and chunksize > 0, \
            f'Chunksize must be a positive integer, is {chunksize}'

        keys_list = list(queries.keys())

        df_dict = {}

        for idx_chunk in range(0, len(keys_list), chunksize):
            keys_chunk = keys_list[idx_chunk:idx_chunk + chunksize]

            json_data = _submit_post_request(
                json_dict=dict(
                    token=get_api_token(),
                    queries={k: queries[k].to_api_struct() for k in keys_chunk}),
                headers=headers,
                timeout=timeout)
            for k, v in json_data['data'].items():
                df_ = pandas.DataFrame(v)
                df_.columns = [c.upper() for c in df_.columns]
                df_dict[k] = df_

        return df_dict


def _submit_post_request(json_dict: dict,
                         timeout: float,
                         headers: Optional[Dict[str, str]] = None) -> dict:
    """
    Submits the POST request and retries on connection errors, waiting longer between each retry

    Parameters
    ----------
    json_dict: dict
    timeout: float
    headers: Optional[Dict[str, str]] = None

    Returns
    -------
    The JSON result from the query in dict form
    """
    for retry_num in range(cc.MAX_RETRIES + 1):
        try:
            r = requests.post(url=cc.API_URL, json=json_dict, headers=headers, timeout=timeout)

            if not r.status_code == 200:
                raise APIQueryFailedException(
                    r.status_code,
                    r.content,
                    {**json_dict, 'token': '**********'})

            json_data = r.json()

            if not json_data['success']:
                raise APIQueryFailedException(json_data)

            return json_data
        except (requests.exceptions.ConnectionError, requests.Timeout) as e:
            if retry_num >= cc.MAX_RETRIES:
                raise e
            else:
                time.sleep(0.5 * (1 + retry_num))
