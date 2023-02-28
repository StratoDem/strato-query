"""
StratoDem Analytics : api_query
Principal Author(s) : Eric Linden, Michael Clawar
Secondary Author(s) :
Description :

Notes :

August 21, 2019
"""

import time
import io

from typing import Dict, Optional, Union, List, Tuple

import requests

import pandas

from strato_query import constants as cc
from .query_structures import *
from .authentication import get_api_token
from .exceptions import APIQueryFailedException

__all__ = ['SDAPIQuery', 'SDJobRunner', 'api_configuration']

T_DF = pandas.DataFrame


api_configuration = {
    'chunksize': 500,
    'timeout': 60.0,
}


class SDAPIQuery:
    @classmethod
    def submit_query(cls,
                     query_params: Optional[APIQueryParams] = None,
                     queries_params: Optional[Dict[str, APIQueryParams]] = None,
                     timeout: Optional[float] = None,
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

        if timeout is None:
            timeout = api_configuration['timeout']

        if query_params is not None:
            return cls.query_api_df(query_params=query_params, headers=headers, timeout=timeout)
        elif queries_params is not None:
            return cls.query_api_multiple(queries=queries_params, headers=headers, timeout=timeout)

    @staticmethod
    def query_api_json(query_params: APIQueryParams,
                       timeout: Optional[float] = None,
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
        if timeout is None:
            timeout = api_configuration['timeout']

        json_data = _submit_post_request(
            json_dict=dict(token=get_api_token(), query=query_params.to_api_struct()),
            headers=headers,
            timeout=timeout)

        return json_data['data'][0]

    @staticmethod
    def query_api_df(query_params: APIQueryParams,
                     timeout: Optional[float] = None,
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
        if timeout is None:
            timeout = api_configuration['timeout']

        json_data = _submit_post_request(
            json_dict=dict(token=get_api_token(), query=query_params.to_api_struct()),
            headers=headers,
            timeout=timeout)

        df_ = pandas.DataFrame(json_data['data'])
        df_.columns = [c.upper() for c in df_.columns]

        return df_

    @staticmethod
    def query_api_multiple(queries: Dict[str, APIQueryParams],
                           timeout: Optional[float] = None,
                           chunksize: int = None,
                           time_between_chunks: Optional[float] = None,
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
        time_between_chunks: Optional[float] = None
            The time (where 1 second is 1.0) to wait between sending chunks
        headers: Optional[Dict[str, str]] = None
            Optional request headers

        Returns
        -------
        A dict with pandas dataframes as the values for each of the query params in the input dict
        """
        if chunksize is None:
            chunksize = api_configuration['chunksize']

        if timeout is None:
            timeout = api_configuration['timeout']

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
            if time_between_chunks is not None and (idx_chunk + chunksize) < len(keys_list):
                time.sleep(time_between_chunks)

        return df_dict


class SDJobRunner:
    def __init__(self, logging: bool = True):
        """
        Job runner to create a data query to the StratoDem Analytics API and get the
        result as a pandas DataFrame

        Parameters
        ----------
        logging: bool
            Noisy logging of process?
        """
        assert isinstance(logging, bool)
        self._logging = logging
        self._job_id = None
        self._response_format = 'csv'

    @property
    def status(self) -> str:
        """Get the status for the job"""
        return self._check_job_status()

    def load_df_from_job_pipeline(self,
                                  model_id: str,
                                  geolevel: Optional[str] = None,
                                  response_format: str = 'csv',
                                  portfolio_id: Optional[str] = None,
                                  market_id: Optional[str] = None,
                                  sites: Optional[List[Tuple[float, float, str]]] = None,
                                  buffers: Optional[List[str]] = None,
                                  geoid_list: Optional[List[int]] = None) -> pandas.DataFrame:
        """
        This method handles all steps of the job pipeline to produce a dataframe, or error if the
        job fails. From a client's request, this method will start a job, and repeatedly check its
        status until it finishes, fails, or the maximum wait time expires. If the job completes,
        this method will download the resulting dataframe and return it to the calling client.

        Parameters
        ----------
        model_id
        geolevel
        response_format
        portfolio_id
        market_id
        sites
        buffers
        geoid_list

        Returns
        -------
        pandas.DataFrame
        """
        self.create_job(
            model_id=model_id,
            geolevel=geolevel,
            response_format=response_format,
            portfolio_id=portfolio_id,
            market_id=market_id,
            sites=sites,
            buffers=buffers,
            geoid_list=geoid_list)

        for idx in range(100):
            if self._logging:
                print('Checking if job is complete...')

            job_status = self.status
            if job_status == 'Completed':
                return self.download_job_to_dataframe()
            elif job_status == 'Processing':
                time.sleep(10)
            else:
                raise APIQueryFailedException('Job failed', job_status)

        raise APIQueryFailedException('Job never completed successfully')

    def create_job(self,
                   model_id: str,
                   geolevel: Optional[str] = None,
                   response_format: str = 'csv',
                   sites: Optional[List[Tuple[float, float, str]]] = None,
                   portfolio_id: Optional[str] = None,
                   market_id: Optional[str] = None,
                   geoid_list: Optional[List[int]] = None,
                   buffers: Optional[List[str]] = None) -> None:
        """
        This method handles the call to create a job through the API, and will log the result of its
        request.

        Parameters
        ----------
        model_id
        geolevel
        response_format
        sites
        portfolio_id
        market_id
        geoid_list
        buffers

        Returns
        -------
        None
        """
        assert isinstance(model_id, str), f'model_id must be str (was {model_id})'
        assert portfolio_id is None or isinstance(portfolio_id, str), \
            f'portfolio_id must be str (was {portfolio_id})'
        assert market_id is None or isinstance(market_id, str), \
            f'market_id must be str (was {market_id})'
        assert geolevel is None or isinstance(geolevel, str), \
            f'geolevel must be str (was {geolevel})'
        assert response_format in {'csv', 'json'}
        assert geoid_list is None or isinstance(geoid_list, list)
        assert geoid_list is None or all(isinstance(geoid, int) for geoid in geoid_list)
        assert buffers is None or isinstance(buffers, list)
        assert buffers is None or all(buffer in cc.BUFFERS_TUPLE for buffer in buffers), \
            f'Invalid buffers: {buffers} (must be from {cc.BUFFERS_TUPLE})'
        assert sites is None or isinstance(sites, list)
        assert sites is None or all(isinstance(site, tuple) for site in sites)

        # Must either be a geolevel, geoid_list combo, or a portfolio_id, or market_id
        if not geolevel and not any([portfolio_id, market_id]):
            raise ValueError('Job requires one of "geolevel", "portfolio_id", or "market_id"')

        if geolevel:
            assert geolevel in {
                'US', 'METRO', 'GEOID2', 'GEOID5', 'ZIP', 'GEOID11', 'site-addresses'}, \
                '"geolevel" must be one of "US", "METRO", "GEOID2", "GEOID5", "ZIP", "GEOID11"'
            assert portfolio_id is None, 'Cannot have both "geolevel" and "portfolio_id"'
            assert market_id is None, 'Cannot have both "geolevel" and "market_id"'

        if geoid_list is None:
            geoid_list = []

        if buffers is None:
            buffers = []

        if sites is None:
            sites = []

        if self._logging:
            print('Sending create job request to API service')

        r = requests.post(
            f'https://{cc.ROUTE_PREFIX}.stratodem.com/jobs/create',
            headers=dict(
                Authorization=f'Bearer {get_api_token()}',
            ),
            json=dict(
                model_id=model_id,
                portfolio_id=portfolio_id,
                market_id=market_id,
                geolevel=geolevel,
                response_format=response_format,
                geoid_list=geoid_list,
                buffers=buffers,
                sites=sites,
            )
        )

        res = r.json()
        if res['success']:
            self._job_id = res['message']['job_id']
            self._response_format = response_format

            if self._logging:
                print('Successfully created job request')
        else:
            raise APIQueryFailedException(res['message'])

    def _check_job_status(self) -> str:
        """
        This method will request the status of the job related to an instance of this class and
        return the status string.

        Returns
        -------
        str
        """
        self._assert_job_created()

        r = requests.post(
            f'https://{cc.ROUTE_PREFIX}.stratodem.com/jobs/status',
            headers=dict(
                Authorization=f'Bearer {get_api_token()}',
            ),
            json=dict(job_id=self._job_id)
        )

        if not r.status_code == 200:
            raise APIQueryFailedException('Failed to determine job status')

        r = r.json()

        if not r['success']:
            raise APIQueryFailedException(r)
        else:
            return r['message']

    def download_job_to_dataframe(self) -> pandas.DataFrame:
        """
        This method will handle the API request to download the job related to an instance of this
        class, and return the dataframe

        Returns
        -------
        pandas.DataFrame
        """
        self._assert_job_created()

        r = requests.post(
            f'https://{cc.ROUTE_PREFIX}.stratodem.com/jobs/download',
            headers=dict(
                Authorization=f'Bearer {get_api_token()}',
            ),
            json=dict(job_id=self._job_id)
        )

        if not r.status_code == 200:
            raise APIQueryFailedException('Failed to download file')

        if self._response_format == 'csv':
            df = pandas.read_csv(io.BytesIO(r.content))
        elif self._response_format == 'json':
            df = pandas.read_json(r.content)
        else:
            raise NotImplementedError(self._response_format)

        return df

    def _assert_job_created(self) -> None:
        assert isinstance(self._job_id, str), 'Must run create_job successfully first ' \
                                              '-- no job id found'


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
                if r.status_code == 520:
                    raise APIQueryFailedException(
                        'Query has timed out. The most likely cause is a query calling for '
                        'too much data at once. Please check the filters and avoid calling for '
                        'unnecessary data.',
                        {**json_dict, 'token': '**********'})
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
                raise APIQueryFailedException(
                    'Query has timed out. The most likely cause is a query calling for '
                    'too much data at once. Please check the filters and avoid calling for '
                    'unnecessary data. Also possible are that the timeout value may have been set '
                    'too low, or a network error could be preventing proper communication with '
                    'the API server.',
                    {**json_dict, 'token': '**********'})
            else:
                time.sleep(0.5 * (1 + retry_num))
