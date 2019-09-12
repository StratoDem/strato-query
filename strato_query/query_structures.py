"""
StratoDem Analytics : queries
Principal Author(s) : Eric Linden, Michael Clawar
Secondary Author(s) :
Description :

Notes :

August 21, 2019
"""

import abc

from typing import List, Tuple, Optional, Union
from .filters import BaseFilter
from .aggregations import BaseAggregation

__all__ = [
    'APIQueryParams',
    'APIMeanQueryParams',
    'APIMedianQueryParams',
    'APIGeoJSONQueryParams',
    'APIPureShapeQueryParams',
    'APIPureShapeUnionQueryParams',
    'APIGeocoderQueryParams',
    'APICalculationQueryParams',
    'APIFilterQueryParams',
]


class APIQueryParams(abc.ABC):
    def __init__(self,
                 data_fields: Union[Tuple[Union[str, dict], ...], List[Union[str, dict]]],
                 table: str,
                 groupby: Union[Tuple[str, ...], List[str]],
                 data_filters: Union[Tuple[Union[dict, BaseFilter], ...],
                                     List[Union[dict, BaseFilter]]],
                 aggregations: Union[Tuple[Union[dict, BaseAggregation], ...],
                                     List[Union[dict, BaseAggregation]]],
                 query_type: Optional[str] = 'COUNT',
                 order: Optional[Union[Tuple[str, ...], List[str]]] = None,
                 on: Optional[dict] = None,
                 join: Optional['APIQueryParams'] = None):
        assert isinstance(data_fields, (tuple, list))
        assert isinstance(table, str)
        assert isinstance(groupby, (tuple, list))
        assert isinstance(data_filters, (tuple, list))
        assert isinstance(aggregations, (tuple, list))
        assert isinstance(query_type, str)
        assert order is None or isinstance(order, (tuple, list))
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
        """
        Converts the query params into a form that the API can work with

        Returns
        -------
        The query params as a dict
        """
        return_dict = dict(
            query_type=self.query_type,
            data_fields=self.data_fields,
            table=self.table,
            groupby=self.groupby,
            data_filters=[f.to_dict() if isinstance(f, BaseFilter) else f
                          for f in self.data_filters],
            aggregations=[agg.to_dict() if isinstance(agg, BaseAggregation) else agg
                          for agg in self.aggregations])

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
    def data_fields(self) -> Union[Tuple[Union[str, dict], ...], List[Union[str, dict]]]:
        return self._data_fields

    @property
    def table(self) -> str:
        return self._table

    @property
    def groupby(self) -> Union[Tuple[str, ...], List[str]]:
        return self._groupby

    @property
    def data_filters(self) -> Union[Tuple[dict, ...], List[dict]]:
        return self._data_filters

    @property
    def aggregations(self) -> Union[Tuple[Union[dict, BaseAggregation], ...],
                                    List[Union[dict, BaseAggregation]]]:
        return self._aggregations

    @property
    def on(self) -> dict:
        return self._on

    @property
    def join(self) -> Union[None, dict]:
        return None if self._join is None else self._join.to_api_struct()

    @property
    def order(self) -> Union[None, Tuple[str, ...], List[str]]:
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
        """
        Converts the query params into a human-readable string representing the Python code

        Returns
        -------
        The query params as a string
        """

        def pretty_print_recursive(query_params, spacer: Optional[str] = '    '):
            dict_form = self._dict_form(query_params)

            if dict_form['query_type'] == 'MEAN':
                query_params_class = 'APIMeanQueryParams'
            elif dict_form['query_type'] == 'MEDIAN':
                query_params_class = 'APIMedianQueryParams'
            elif dict_form['query_type'] == 'FILTER':
                query_params_class = 'APIFilterQueryParams'
            elif dict_form['query_type'] == 'CALCULATION':
                query_params_class = 'APICalculationQueryParams'
            elif dict_form['query_type'] == 'GEOJSON':
                query_params_class = 'APIGeoJSONQueryParams'
            else:
                query_params_class = 'APIQueryParams'

            string_form = '''{query_params_class}(
{spacer}table='{table_name}',
{spacer}data_fields={fields},
{spacer}data_filters={filters},
{spacer}query_type='{query_type}',
{spacer}aggregations={aggregations},
{spacer}groupby={groupby},{inner_query}{mean_value}{median_value}{order}{on}{join}
{spacer})'''.format(
                query_params_class=query_params_class,
                table_name=dict_form['table'],
                fields=dict_form['data_fields'],
                filters=dict_form['data_filters'],
                query_type=dict_form['query_type'],
                aggregations=dict_form['aggregations'],
                groupby=dict_form['groupby'],
                inner_query='\n{spacer}inner_query={var},'.format(
                    spacer=spacer,
                    var=pretty_print_recursive(
                        query_params=dict_form['inner_query'],
                        spacer=spacer + '    ')
                ) if 'inner_query' in dict_form else '',
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
        """
        Converts the query params into a human-readable string representing the VBA code

        Returns
        -------
        The query params as a string
        """

        def pretty_print_recursive(query_params, spacer: Optional[str] = '    ') -> str:
            dict_form = self._dict_form(query_params)

            if dict_form['query_type'] == 'MEAN':
                query_params_func = 'meanQueryParameters'
            elif dict_form['query_type'] == 'MEDIAN':
                query_params_func = 'medianQueryParameters'
            elif dict_form['query_type'] == 'FILTER':
                query_params_func = 'filterQueryParameters'
            elif dict_form['query_type'] == 'CALCULATION':
                query_params_func = 'calculationQueryParameters'
            elif dict_form['query_type'] == 'GEOJSON':
                query_params_func = 'geoJSONQueryParameters'
            else:
                query_params_func = 'apiQueryParameters'

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
{spacer}groupby:=Array({groupby}){order}{inner_query}{median}{mean}{on}{join}{query_type})
'''.format(
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
                inner_query=', _\n{spacer}join:={var}'.format(
                    spacer=spacer,
                    var=pretty_print_recursive(
                        query_params=dict_form['inner_query'],
                        spacer=spacer + '    ')
                ) if 'inner_query' in dict_form else '',
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
        """
        Converts the query params into a human-readable string representing the R code

        Returns
        -------
        The query params as a string
        """

        def pretty_print_recursive(query_params, spacer: Optional[str] = '  ') -> str:
            dict_form = self._dict_form(query_params)

            if dict_form['query_type'] == 'MEAN':
                query_params_func = 'mean_query_params'
            elif dict_form['query_type'] == 'MEDIAN':
                query_params_func = 'median_query_params'
            elif dict_form['query_type'] == 'FILTER':
                query_params_func = 'filter_query_params'
            elif dict_form['query_type'] == 'CALCULATION':
                query_params_func = 'calculation_query_params'
            elif dict_form['query_type'] == 'GEOJSON':
                query_params_func = 'geoJSON_query_params'
            else:
                query_params_func = 'api_query_params'

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
{spacer}groupby = c({groupby}){mean_value}{median_value}{order}{on}{inner_query}{join}{query_type})
'''.format(
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
                inner_query=',\n{spacer}join = {var}'.format(
                    spacer=spacer,
                    var=pretty_print_recursive(
                        query_params=dict_form['inner_query'],
                        spacer=spacer + '    ')
                ) if 'inner_query' in dict_form else '',
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
        """
        Converts the query params into a form that the API can work with

        Returns
        -------
        The query params as a dict
        """
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
        """
        Converts the query params into a form that the API can work with

        Returns
        -------
        The query params as a dict
        """
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
    def __init__(self,
                 properties: Union[Tuple[Union[str, dict], ...], List[Union[str, dict]]],
                 **kwargs):
        assert isinstance(properties, (list, tuple))

        super().__init__(**kwargs)

        self._properties = properties

    def to_api_struct(self):
        """
        Converts the query params into a form that the API can work with

        Returns
        -------
        The query params as a dict
        """
        return_dict = super().to_api_struct()
        return_dict['properties'] = self.properties

        return return_dict

    @property
    def query_type(self) -> str:
        return 'GEOJSON'

    @property
    def properties(self) -> Tuple[Union[str, dict], ...]:
        return self._properties


class APIPureShapeQueryParams(APIGeoJSONQueryParams):
    @property
    def query_type(self) -> str:
        return 'PURE_SHAPE'


class APIPureShapeUnionQueryParams(APIGeoJSONQueryParams):
    def __init__(self, join: List['APIQueryParams'], **kwargs):
        assert isinstance(join, list)

        super().__init__(**kwargs)

        self._join = join

    @property
    def query_type(self) -> str:
        return 'SHAPES_UNION'

    @property
    def join(self) -> Union[None, List[APIQueryParams]]:
        return None if self._join is None else self._join


class APIGeocoderQueryParams(APIQueryParams):
    def __init__(self, latitude: Union[int, float], longitude: Union[int, float], **kwargs):
        assert isinstance(latitude, (int, float))
        assert isinstance(longitude, (int, float))

        super().__init__(**kwargs)

        self._latitude = latitude
        self._longitude = longitude

    def to_api_struct(self) -> dict:
        """
        Converts the query params into a form that the API can work with

        Returns
        -------
        The query params as a dict
        """
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


class APICalculationQueryParams(APIQueryParams):
    def __init__(self, inner_query: 'APIQueryParams', **kwargs):
        super().__init__(**kwargs)

        self._inner_query = inner_query

    def to_api_struct(self) -> dict:
        """
        Converts the query params into a form that the API can work with

        Returns
        -------
        The query params as a dict
        """
        return_dict = super().to_api_struct()
        return_dict['inner_query'] = self.inner_query

        return return_dict

    @property
    def query_type(self) -> str:
        return 'CALCULATION'

    @property
    def inner_query(self) -> dict:
        return self._inner_query.to_api_struct()


class APIFilterQueryParams(APICalculationQueryParams):
    @property
    def query_type(self) -> str:
        return 'FILTER'
