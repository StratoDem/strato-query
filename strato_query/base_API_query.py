"""
StratoDem Analytics : base_API_query
Principal Author(s) : Eric Linden
Secondary Author(s) : 
Description :

Notes : 

December 26, 2018
"""

import abc
from typing import Tuple, Dict, Optional, Union, List

import requests


class APIQueryParams(abc.ABC):
    def __init__(self,
                 data_fields: Tuple[Union[str, dict], ...],
                 table: str,
                 groupby: Tuple[str, ...],
                 data_filters: Tuple[dict, ...],
                 aggregations: Tuple[dict, ...],
                 query_type: str):
        assert isinstance(data_fields, tuple)
        assert isinstance(table, str)
        assert isinstance(groupby, tuple)
        assert isinstance(data_filters, tuple)
        assert isinstance(aggregations, tuple)
        assert isinstance(query_type, str)

        self._query_type = query_type
        self._data_fields = data_fields
        self._table = table
        self._groupby = groupby
        self._data_filters = data_filters
        self._aggregations = aggregations

    def to_api_struct(self) -> dict:
        return dict(
            query_type=self.query_type,
            data_fields=self.data_fields,
            table=self.table,
            groupby=self.groupby,
            data_filters=self.data_filters,
            aggregations=self.aggregations)

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


class APIJoinParam(APIQueryParams):
    def __init__(self, on: dict, **kwargs):
        assert isinstance(on, dict)

        self._on = on

        super().__init__(**kwargs)

    def to_api_struct(self) -> dict:
        return dict(
            query_type=self.query_type,
            data_fields=self.data_fields,
            table=self.table,
            groupby=self.groupby,
            data_filters=self.data_filters,
            aggregations=self.aggregations,
            on=self.on)

    @property
    def on(self) -> dict:
        return self._on


class APIJoinQueryParams(APIQueryParams):
    def __init__(self, join: APIJoinParam, **kwargs):
        assert isinstance(join, APIJoinParam)

        self._join = join

        super().__init__(**kwargs)

    def to_api_struct(self) -> dict:
        return dict(
            query_type=self.query_type,
            data_fields=self.data_fields,
            table=self.table,
            groupby=self.groupby,
            data_filters=self.data_filters,
            aggregations=self.aggregations,
            join=self.join)

    @property
    def join(self) -> dict:
        return self._join.to_api_struct()


class BaseAPIQuery:
    @classmethod
    def submit_query(cls, query_params: Optional[APIQueryParams]=None,
                     queries_params: Optional[Dict[str, APIQueryParams]]=None) -> Union[T_DF, Dict[str, T_DF]]:
        assert query_params is None or isinstance(query_params, APIQueryParams)
        assert queries_params is None or isinstance(queries_params, APIQueryParams)
        assert not(query_params is None and queries_params is None)
        assert not(query_params is not None and queries_params is not None)

        if query_params is not None:
            return cls.query_api_df(query_params=query_params)
        elif queries_params is not None:
            return cls.query_api_multiple(queries=queries_params)

    @staticmethod
    def query_api_df(query_params: APIQueryParams) -> pandas.DataFrame:
        r = requests.post(
            url=SDConfig.api_url,
            json=dict(
                token=SDConfig.api_token,
                query=query_params.to_api_struct()))

        assert r.status_code == 200, (r.status_code, r.content, query_params.to_api_struct())

        json_data = r.json()
        assert json_data['success'], json_data

        df_ = pandas.DataFrame(json_data['data'])
        df_.columns = [c.upper() for c in df_.columns]

        return df_

    @staticmethod
    def query_api_multiple(queries: Dict[str, APIQueryParams]) -> Dict[str, pandas.DataFrame]:
        r = requests.post(
            url=SDConfig.api_url,
            json=dict(
                token=SDConfig.api_token,
                queries={k: v.to_api_struct() for k, v in queries.items()}))

        assert r.status_code == 200, (r.status_code, r.content, queries)

        json_data = r.json()
        assert json_data['success'], json_data

        df_dict = {}
        for k, v in json_data['data'].items():
            df_ = pandas.DataFrame(v)
            df_.columns = [c.upper() for c in df_.columns]
            df_dict[k] = df_

        return df_dict