"""
StratoDem Analytics : base_API_query
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

December 26, 2018
"""

import abc
import os
from typing import Tuple, Dict, Optional, Union, List

import requests

import pandas

import config as sdc

from strato_query.core import constants as cc


__all__ = [
    'APIQueryParams', 'BaseAPIQuery', 'APIMeanQueryParams', 'APIMedianQueryParams',
]

API_TOKEN = os.environ.get('API_TOKEN', sdc.debug_token)
T_DF = pandas.DataFrame


class APIQueryParams(abc.ABC):
    def __init__(self,
                 data_fields: Tuple[Union[str, dict], ...],
                 table: str,
                 groupby: Tuple[str, ...],
                 data_filters: Tuple[dict, ...],
                 aggregations: Tuple[dict, ...],
                 query_type: str,
                 order: Optional[Tuple[str, ...]] = None,
                 on: Optional[dict] = None,
                 join: Optional['APIQueryParams'] = None):
        assert isinstance(data_fields, tuple)
        assert isinstance(table, str)
        assert isinstance(groupby, tuple)
        assert isinstance(data_filters, tuple)
        assert isinstance(aggregations, tuple)
        assert isinstance(query_type, str)
        assert order is None or isinstance(order, tuple)
        assert on is None or isinstance(on, dict)

        self._query_type = query_type
        self._data_fields = data_fields
        self._table = table
        self._groupby = groupby
        self._data_filters = data_filters
        self._aggregations = aggregations
        self._on = on
        self._join = join
        self._order = order

    def to_api_struct(self) -> dict:
        return_dict = dict(
            query_type=self.query_type,
            data_fields=self.data_fields,
            table=self.table,
            groupby=self.groupby,
            data_filters=self.data_filters,
            aggregations=self.aggregations)

        if self.on is not None:
            return_dict['on'] = self.on
        if self.join is not None:
            return_dict['join'] = self.join
        if self.order is not None:
            return_dict['order'] = self.order

        return return_dict

    # /// Properties
    @property
    def query_type(self) -> str:
        return self._query_type

    @property
    def data_fields(self) -> Tuple[Union[str, dict], ...]:
        return self._data_fields

    @property
    def table(self) -> str:
        return self._table

    @property
    def groupby(self) -> Tuple[str, ...]:
        return self._groupby

    @property
    def data_filters(self) -> Tuple[dict, ...]:
        return self._data_filters

    @property
    def aggregations(self) -> Tuple[dict, ...]:
        return self._aggregations

    @property
    def on(self) -> dict:
        return self._on

    @property
    def join(self) -> Union[None, dict]:
        return None if self._join is None else self._join.to_api_struct()

    @property
    def order(self) -> Union[None, Tuple[str, ...]]:
        return self._order


class APIMeanQueryParams(APIQueryParams):
    def __init__(self, mean_variable_name: str, **kwargs):
        assert isinstance(mean_variable_name, str)

        self._mean_variable_name = mean_variable_name

        super().__init__(**kwargs)

    def to_api_struct(self):
        return_dict = super().to_api_struct()
        return_dict['mean_variable_name'] = self.mean_variable_name

        return return_dict

    @property
    def mean_variable_name(self) -> str:
        return self._mean_variable_name


class APIMedianQueryParams(APIQueryParams):
    def __init__(self, median_variable_name: str, **kwargs):
        assert isinstance(median_variable_name, str)

        self._median_variable_name = median_variable_name

        super().__init__(**kwargs)

    def to_api_struct(self):
        return_dict = super().to_api_struct()
        return_dict['median_variable_name'] = self.median_variable_name

        return return_dict

    @property
    def median_variable_name(self) -> str:
        return self._median_variable_name


class BaseAPIQuery:
    @classmethod
    def submit_query(cls, query_params: Optional[APIQueryParams] = None,
                     queries_params: Optional[Dict[str, APIQueryParams]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Union[T_DF, Dict[str, T_DF]]:
        assert query_params is None or isinstance(query_params,
                                                  APIQueryParams)
        assert queries_params is None or isinstance(queries_params,
                                                    APIQueryParams)
        assert not(query_params is None and queries_params is None)
        assert not(query_params is not None and queries_params is not None)

        if query_params is not None:
            return cls.query_api_df(query_params=query_params, headers=headers)
        elif queries_params is not None:
            return cls.query_api_multiple(queries=queries_params, headers=headers)

    @staticmethod
    def query_api_df(query_params: APIQueryParams,
                     headers: Optional[Dict[str, str]] = None) -> pandas.DataFrame:
        r = requests.post(
            url=cc.API_URL,
            json=dict(
                token=API_TOKEN,
                query=query_params.to_api_struct()),
            headers=headers)

        assert r.status_code == 200, (r.status_code,
                                      r.content,
                                      query_params.to_api_struct())

        json_data = r.json()
        assert json_data['success'], json_data

        df_ = pandas.DataFrame(json_data['data'])
        df_.columns = [c.upper() for c in df_.columns]

        return df_

    @staticmethod
    def query_api_multiple(queries: Dict[str, APIQueryParams],
                           headers: Optional[Dict[str, str]] = None) -> Dict[str, pandas.DataFrame]:
        r = requests.post(
            url=cc.API_URL,
            json=dict(
                token=API_TOKEN,
                queries={k: v.to_api_struct() for k, v in queries.items()}),
            headers=headers)

        assert r.status_code == 200, (r.status_code, r.content, queries)

        json_data = r.json()
        assert json_data['success'], json_data

        df_dict = {}
        for k, v in json_data['data'].items():
            df_ = pandas.DataFrame(v)
            df_.columns = [c.upper() for c in df_.columns]
            df_dict[k] = df_

        return df_dict


if __name__ == '__main__':
    print(BaseAPIQuery.submit_query(
        query_params=APIQueryParams(
            query_type='COUNT',
            data_fields=('year', 'population'),
            table='populationforecast_us_annual_population_age',
            data_filters=(
                dict(filter_type='eq',
                     filter_variable='age_g',
                     filter_value=18),
                dict(filter_type='between',
                     filter_variable='year',
                     filter_value=[2013, 2018])
            ),
            aggregations=(dict(aggregation_func='sum',
                               variable_name='population'),),
            groupby=('year',),
        )))
