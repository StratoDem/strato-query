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
import time

from typing import Tuple, Dict, Optional, Union

import requests

import pandas

from strato_query.core import constants as cc

__all__ = [
    'APIQueryParams',
    'BaseAPIQuery',
    'APIMeanQueryParams',
    'APIMedianQueryParams',
    'APIGeoJSONQueryParams',
    'APIGeocoderQueryParams',
]

API_TOKEN = os.environ.get('API_TOKEN')
if API_TOKEN is None:
    raise ValueError('No API token provided via API_TOKEN environment variable')

T_DF = pandas.DataFrame


class APIQueryParams(abc.ABC):
    def __init__(self,
                 data_fields: Tuple[Union[str, dict], ...],
                 table: str,
                 groupby: Tuple[str, ...],
                 data_filters: Tuple[dict, ...],
                 aggregations: Tuple[dict, ...],
                 query_type: Optional[str] = 'COUNT',
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

    @staticmethod
    def _dict_form(query_params) -> dict:
        if isinstance(query_params, APIQueryParams):
            dict_form = query_params.to_api_struct()
        elif isinstance(query_params, dict):
            dict_form = query_params
        else:
            raise ValueError(query_params)

        return dict_form

    def pretty_print(self) -> str:
        def pretty_print_recursive(query_params, spacer: Optional[str] = '    '):
            dict_form = self._dict_form(query_params)
            query_params_class = 'APIQueryParams'
            if 'mean_variable_name' in dict_form:
                query_params_class = 'APIMeanQueryParams'
            elif 'median_variable_name' in dict_form:
                query_params_class = 'APIMedianQueryParams'

            string_form = '''{query_params_class}(
{spacer}table='{table_name}',
{spacer}data_fields={fields},
{spacer}data_filters={filters},
{spacer}query_type='{query_type}',
{spacer}aggregations={aggregations},
{spacer}groupby={groupby},{mean_value}{median_value}{order}{on}{join}
{spacer})'''.format(
                query_params_class=query_params_class,
                table_name=dict_form['table'],
                fields=dict_form['data_fields'],
                filters=dict_form['data_filters'],
                query_type=dict_form['query_type'],
                aggregations=dict_form['aggregations'],
                groupby=dict_form['groupby'],
                mean_value='\n{spacer}mean_variable_name=\'{var}\','.format(
                    spacer=spacer,
                    var=dict_form['mean_variable_name']
                ) if 'mean_variable_name' in dict_form else '',
                median_value='\n{spacer}median_variable_name=\'{var}\','.format(
                    spacer=spacer,
                    var=dict_form['median_variable_name']
                ) if 'median_variable_name' in dict_form else '',
                order='\n{spacer}order={var},'.format(
                    spacer=spacer,
                    var=dict_form['order']) if 'order' in dict_form else '',
                join='\n{spacer}join={var}'.format(
                    spacer=spacer,
                    var=pretty_print_recursive(
                        query_params=dict_form['join'],
                        spacer=spacer + '    ')
                ) if 'join' in dict_form else '',
                on='\n{spacer}on={var},'.format(
                    spacer=spacer,
                    var=dict_form['on']) if 'on' in dict_form else '',
                spacer=spacer)

            return string_form

        return pretty_print_recursive(query_params=self)

    def pretty_print_vba(self) -> str:
        def pretty_print_recursive(query_params, spacer: Optional[str] = '    ') -> str:
            dict_form = self._dict_form(query_params)
            query_params_func = 'apiQueryParameters'
            if 'mean_variable_name' in dict_form:
                query_params_func = 'meanQueryParameters'
            if 'median_variable_name' in dict_form:
                query_params_func = 'medianQueryParameters'

            def _process_renamed_field(field: dict) -> str:
                assert isinstance(field, dict)

                original = list(field.keys())[0]
                renamed = field[original]

                renamed_val = '"{}"'.format(renamed) if isinstance(renamed, str) else renamed

                return 'renameVariable(original:="{}", renamed:={})'.format(original, renamed_val)

            def _process_filter(filt: dict) -> str:
                assert isinstance(filt, dict)

                filter_type = filt['filter_type']
                if filter_type in {'mile_radius', 'drivetime'}:
                    metric = 'miles' if filter_type == 'mile_radius' else 'minutes'
                    func = {
                        'mile_radius': 'mileRadiusFilter',
                        'drivetime': 'drivetimeFilter'}[filter_type]
                    return '{func}(latitude:={lat}, longitude:={lng}, {metric}:={val})'.format(
                        func=func,
                        lat=filt['filter_value']['latitude'],
                        lng=filt['filter_value']['longitude'],
                        metric=metric,
                        val=filt['filter_value'][metric]
                    )
                else:
                    func = {
                        'eq': 'equalToFilter',
                        'ne': 'notEqualToFilter',
                        'gt': 'greaterThanFilter',
                        'ge': 'greaterThanOrEqualToFilter',
                        'lt': 'lessThanFilter',
                        'le': 'lessThanOrEqualToFilter',
                        'in': 'inFilter',
                        'nin': 'notInFilter',
                        'between': 'betweenFilter',
                    }[filter_type]

                    fv = filt['filter_value']
                    if isinstance(fv, str):
                        filter_value = '"{}"'.format(fv)
                    elif isinstance(fv, (list, tuple)):
                        filter_value = 'Array({})'.format(
                            ', '.join('"{}"'.format(v) if isinstance(v, str) else str(v)
                                      for v in fv))
                    else:
                        filter_value = fv
                    return '{func}(filterVariable:="{filter_variable}", ' \
                           'filterValue:={filter_value})'.format(
                            func=func,
                            filter_variable=filt['filter_variable'],
                            filter_value=filter_value)

            def _process_aggregation(agg: dict) -> str:
                assert isinstance(agg, dict)

                aggregation_func = agg['aggregation_func']
                variable_name = agg['variable_name']

                return '{}Aggregation(variableName:="{}")'.format(aggregation_func, variable_name)

            def _process_join_on(on: dict) -> str:
                assert isinstance(on, dict)
                left = on['left']
                right = on['right']

                return 'joinOnStructure(left:=Array({}), right:=Array({}))'.format(
                    ', '.join('"{}"'.format(f) for f in left),
                    ', '.join('"{}"'.format(f) for f in right))

            return '''{query_params_func}( _
{spacer}table:="{table_name}", _
{spacer}dataFields:=Array({fields}), _
{spacer}dataFilters:=Array({filters}), _
{spacer}aggregations:=Array({aggregations}), _
{spacer}groupby:=Array({groupby}){order}{median}{mean}{on}{join}{query_type})'''.format(
                query_params_func=query_params_func,
                table_name=dict_form['table'],
                fields=', '.join(
                    '"{}"'.format(f) if isinstance(f, str) else _process_renamed_field(f)
                    for f in dict_form['data_fields']),
                filters=', '.join(_process_filter(f) for f in dict_form['data_filters']),
                aggregations=', '.join(_process_aggregation(agg)
                                       for agg in dict_form['aggregations']),
                groupby=', '.join('"{}"'.format(f) for f in dict_form['groupby']),
                order=', order:=Array({var})'.format(
                    spacer=spacer,
                    var=', '.join('"{}"'.format(f) for f in dict_form['order']))
                if 'order' in dict_form else '',
                mean=', _\n{spacer}meanVariableName:="{var}"'.format(
                    spacer=spacer,
                    var=dict_form['mean_variable_name']
                ) if 'mean_variable_name' in dict_form else '',
                median=', _\n{spacer}medianVariableName:="{var}"'.format(
                    spacer=spacer,
                    var=dict_form['median_variable_name']
                ) if 'median_variable_name' in dict_form else '',
                join=', _\n{spacer}join:={var}'.format(
                    spacer=spacer,
                    var=pretty_print_recursive(
                        query_params=dict_form['join'],
                        spacer=spacer + '    ')) if 'join' in dict_form else '',
                on=', _\n{spacer}joinOn:={joinOn}'.format(
                    spacer=spacer,
                    joinOn=_process_join_on(dict_form['on'])) if 'on' in dict_form else '',
                query_type=', _\n{spacer}queryType:="{query_type}"'.format(
                    spacer=spacer, query_type=dict_form['query_type'])
                if 'query_type' in dict_form and query_params_func == 'apiQueryParameters' else '',
                spacer=spacer)

        return pretty_print_recursive(query_params=self)

    def pretty_print_r(self) -> str:
        def pretty_print_recursive(query_params, spacer: Optional[str] = '  ') -> str:
            dict_form = self._dict_form(query_params)
            query_params_func = 'api_query_params'
            if 'mean_variable_name' in dict_form:
                query_params_func = 'mean_query_params'
            elif 'median_variable_name' in dict_form:
                query_params_func = 'median_query_params'

            def _process_field(field: Union[str, dict]) -> str:
                if isinstance(field, str):
                    return "'{field}'".format(field=field)
                elif isinstance(field, dict):
                    k = list(field.keys())[0]
                    v = field[k]
                    return "list('{}' = '{}')".format(k, v)
                else:
                    raise TypeError(field)

            def _process_filter(filt: dict) -> str:
                assert isinstance(filt, dict)

                filter_type = filt['filter_type']
                if filter_type in {'mile_radius', 'drivetime'}:
                    metric = 'miles' if filter_type == 'mile_radius' else 'minutes'
                    func = {
                        'mile_radius': 'mile_radius_filter',
                        'drivetime': 'drivetime_filter'}
                    return '{func}(latitude = {lat}, longitude = {lng}, {metric} = {val})'.format(
                        func=func,
                        lat=filt['filter_value']['latitude'],
                        lng=filt['filter_value']['longitude'],
                        metric=metric,
                        val=filt['filter_value'][metric]
                    )
                else:
                    func = {
                        'eq': 'eq_filter',
                        'ne': 'ne_filter',
                        'gt': 'gt_filter',
                        'ge': 'ge_filter',
                        'lt': 'lt_filter',
                        'le': 'le_filter',
                        'in': 'in_filter',
                        'nin': 'nin_filter',
                        'between': 'between_filter',
                    }[filter_type]

                    fv = filt['filter_value']
                    if isinstance(fv, str):
                        filter_value = '"{}"'.format(fv)
                    elif isinstance(fv, (list, tuple)):
                        filter_value = 'c({})'.format(
                            ', '.join('"{}"'.format(v) if isinstance(v, str) else str(v)
                                      for v in fv))
                    else:
                        filter_value = fv
                    return '{func}(filter_variable = "{filter_variable}", ' \
                           'filter_value = {filter_value})'.format(
                            func=func,
                            filter_variable=filt['filter_variable'],
                            filter_value=filter_value)

            def _process_aggregation(agg: dict) -> str:
                assert isinstance(agg, dict)

                aggregation_func = agg['aggregation_func']
                variable_name = agg['variable_name']

                return '{}_aggregation(variable_name = "{}")'.format(
                    aggregation_func, variable_name)

            string_form = '''{query_params_func}(
{spacer}table = '{table_name}',
{spacer}data_fields = api_fields(fields_list = list({fields})),
{spacer}data_filters = list({filters}),
{spacer}aggregations = list({aggregations}),
{spacer}groupby = c({groupby}){mean_value}{median_value}{order}{on}{join}{query_type})'''.format(
                query_params_func=query_params_func,
                table_name=dict_form['table'],
                fields=', '.join(_process_field(f) for f in dict_form['data_fields']),
                filters=', '.join(_process_filter(f) for f in dict_form['data_filters']),
                aggregations=', '.join(_process_aggregation(agg)
                                       for agg in dict_form['aggregations']),
                groupby=', '.join('"{}"'.format(f) for f in dict_form['groupby']),
                order=',\n{spacer}order = c({var})'.format(
                    spacer=spacer,
                    var=', '.join('"{}"'.format(f) for f in dict_form['order']))
                if 'order' in dict_form else '',
                mean_value=',\n{spacer}mean_variable_name = \'{var}\''.format(
                    spacer=spacer,
                    var=dict_form['mean_variable_name']
                ) if 'mean_variable_name' in dict_form else '',
                median_value=',\n{spacer}median_variable_name = \'{var}\''.format(
                    spacer=spacer,
                    var=dict_form['median_variable_name']
                ) if 'median_variable_name' in dict_form else '',
                join=',\n{spacer}join = {var}'.format(
                    spacer=spacer,
                    var=pretty_print_recursive(
                        query_params=dict_form['join'],
                        spacer=spacer + '    ')
                ) if 'join' in dict_form else '',
                on=',\n{spacer}on = list(left = c({left}), right = c({right}))'.format(
                    spacer=spacer,
                    left=', '.join("'{}'".format(f) for f in dict_form['on']['left']),
                    right=', '.join("'{}'".format(f) for f in dict_form['on']['right']))
                if 'on' in dict_form else '',
                query_type=',\n{spacer}query_type = "{query_type}"'.format(
                    spacer=spacer, query_type=dict_form['query_type'])
                if 'query_type' in dict_form and query_params_func == 'api_query_params' else '',
                spacer=spacer)

            return string_form

        return pretty_print_recursive(query_params=self)


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
    def query_type(self) -> str:
        return 'MEAN'

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
    def query_type(self) -> str:
        return 'MEDIAN'

    @property
    def median_variable_name(self) -> str:
        return self._median_variable_name


class APIGeoJSONQueryParams(APIQueryParams):
    def __init__(self, properties: Tuple[Union[str, dict], ...], **kwargs):
        assert isinstance(properties, tuple)

        super().__init__(**kwargs)

        self._properties = properties

    def to_api_struct(self):
        return_dict = super().to_api_struct()
        return_dict['properties'] = self.properties

        return return_dict

    @property
    def query_type(self) -> str:
        return 'GEOJSON'

    @property
    def properties(self) -> Tuple[Union[str, dict], ...]:
        return self._properties


class APIGeocoderQueryParams(APIQueryParams):
    def __init__(self, latitude: Union[int, float], longitude: Union[int, float], **kwargs):
        assert isinstance(latitude, (int, float))
        assert isinstance(longitude, (int, float))

        super().__init__(**kwargs)

        self._latitude = latitude
        self._longitude = longitude

    def to_api_struct(self):
        return_dict = super().to_api_struct()
        return_dict['latitude'] = self.latitude
        return_dict['longitude'] = self.longitude

        return return_dict

    @property
    def query_type(self) -> str:
        return 'GEOCODER'

    @property
    def latitude(self) -> Union[float, int]:
        return self._latitude

    @property
    def longitude(self) -> Union[float, int]:
        return self._longitude


class BaseAPIQuery:
    @classmethod
    def submit_query(cls, query_params: Optional[APIQueryParams] = None,
                     queries_params: Optional[Dict[str, APIQueryParams]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Union[T_DF, Dict[str, T_DF]]:
        assert query_params is None or isinstance(query_params,
                                                  APIQueryParams)
        assert queries_params is None or isinstance(queries_params,
                                                    APIQueryParams)
        assert not (query_params is None and queries_params is None)
        assert not (query_params is not None and queries_params is not None)

        if query_params is not None:
            return cls.query_api_df(query_params=query_params, headers=headers)
        elif queries_params is not None:
            return cls.query_api_multiple(queries=queries_params, headers=headers)

    @staticmethod
    def query_api_json(query_params: APIQueryParams,
                       headers: Optional[Dict[str, str]] = None) -> dict:
        json_data = _submit_post_request(
            json_dict=dict(token=API_TOKEN, query=query_params.to_api_struct()),
            headers=headers)

        return json_data['data'][0]

    @staticmethod
    def query_api_df(query_params: APIQueryParams,
                     headers: Optional[Dict[str, str]] = None) -> pandas.DataFrame:
        json_data = _submit_post_request(
            json_dict=dict(token=API_TOKEN, query=query_params.to_api_struct()),
            headers=headers)

        df_ = pandas.DataFrame(json_data['data'])
        df_.columns = [c.upper() for c in df_.columns]

        return df_

    @staticmethod
    def query_api_multiple(queries: Dict[str, APIQueryParams],
                           headers: Optional[Dict[str, str]] = None) -> Dict[str, pandas.DataFrame]:
        json_data = _submit_post_request(
            json_dict=dict(
                token=API_TOKEN,
                queries={k: v.to_api_struct() for k, v in queries.items()}),
            headers=headers)

        df_dict = {}
        for k, v in json_data['data'].items():
            df_ = pandas.DataFrame(v)
            df_.columns = [c.upper() for c in df_.columns]
            df_dict[k] = df_

        return df_dict


def _submit_post_request(json_dict: dict, headers: Optional[Dict[str, str]] = None):
    for retry_num in range(cc.MAX_RETRIES):
        try:
            r = requests.post(url=cc.API_URL, json=json_dict, headers=headers)

            assert r.status_code == 200, (r.status_code, r.content, json_dict)

            json_data = r.json()
            assert json_data['success'], json_data

            return json_data
        except requests.exceptions.ConnectionError as e:
            if retry_num == cc.MAX_RETRIES - 1:
                raise e
            else:
                time.sleep(0.1 * (1 + retry_num))


if __name__ == '__main__':
    print(
        BaseAPIQuery.query_api_df(
            query_params=APIGeocoderQueryParams(
                data_fields=('geoid11', 'geoid5',),
                table='geocookbook_tract_na_shapes_full',
                data_filters=(),
                groupby=(),
                aggregations=(),
                latitude=42.983899,
                longitude=-99.306204)))
