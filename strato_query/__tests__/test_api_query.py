"""
StratoDem Analytics : test_api_query
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

December 26, 2018
"""

import unittest

from strato_query import *


class TestAPIQuery(unittest.TestCase, SDAPIQuery):
    age_filter = NotInFilter(
        var='age_g_bottom_coded',
        val=[16, 17, 18]).to_dict()
    year_filter = EqualToFilter(
        var='year',
        val=2015).to_dict()

    def setUp(self) -> None:
        authenticate_to_api()

    def test_query_call(self):
        from strato_query.exceptions import APIQueryFailedException

        age_filter = EqualToFilter(
            var='age_g',
            val=18)

        year_filter = BetweenFilter(
            var='year',
            val=[2013, 2018]).to_dict()

        df = self.submit_query(
            query_params=APIQueryParams(
                data_fields=('year', 'population'),
                table='populationforecast_us_annual_population_age',
                data_filters=(age_filter, year_filter),
                aggregations=[SumAggregation('population')],
                groupby=('year',),
            ),
        )

        df_sorted = df.sort_values(by='YEAR', ascending=True)
        assert all(x == y for x, y in zip(
            df_sorted['YEAR'].values, [x for x in range(2013, 2019)]))

        with self.assertRaises(APIQueryFailedException):
            df = self.submit_query(
                query_params=APIQueryParams(
                    data_fields=('year', 'population'),
                    table='populationforecast_us_annual_population_age',
                    data_filters=(age_filter, year_filter),
                    aggregations=(dict(aggregation_func='sum',
                                       variable_name='population'),),
                    groupby=('year',),
                ),
                timeout=0.000001
            )

    def test_multi_join(self):
        df = self.query_api_df(
            query_params=APIQueryParams(
                table='geocookbook_county_na_county_metro',
                data_fields=('GEOID5',),
                data_filters=(InFilter(var='cbsa', val=[14454]).to_dict(),),
                aggregations=(),
                groupby=(),
                join=APIQueryParams(
                    table='geocookbook_county_na_county_name',
                    data_fields=('GEOID5', 'GEOID2', 'GEOID5_NAME'),
                    data_filters=(),
                    aggregations=(),
                    groupby=(),
                    on=dict(left=('GEOID5',), right=('GEOID5',)),
                    join=APIQueryParams(
                        table='geocookbook_state_na_state_name',
                        data_fields=('GEOID2', 'GEOID2_INIT'),
                        data_filters=(),
                        aggregations=(),
                        groupby=(),
                        on=dict(left=('GEOID2',), right=('GEOID2',)),
                    )
                )
            )
        )

        df['NAME'] = df['GEOID5_NAME'] + ', ' + df['GEOID2_INIT']

        assert len(df) == 3
        assert df['GEOID5'].values[1] == 25023
        assert df['NAME'].values[1] == 'Plymouth County, MA'

    def test_multi_query(self):
        df_dict = self.submit_query(
            queries_params=dict(
                query_1=APIQueryParams(
                    table='geocookbook_county_na_county_metro',
                    data_fields=('GEOID5',),
                    data_filters=[InFilter(var='cbsa', val=[14454])],
                    aggregations=(),
                    groupby=()),
                query_2=APIQueryParams(
                    table='geocookbook_county_na_county_name',
                    data_fields=('GEOID5', 'GEOID2', 'GEOID5_NAME'),
                    data_filters=(),
                    aggregations=(),
                    groupby=(),
                    on=dict(left=('GEOID5',), right=('GEOID5',))),
            )
        )

        assert len(df_dict) == 2
        assert len(df_dict['query_1']['GEOID5'].values) == 3
        assert len(df_dict['query_2']['GEOID5'].values) == 3104

    def test_median_query(self):
        year_filter = GreaterThanOrEqualToFilter(
            var='year',
            val=2013)

        df = self.submit_query(
            query_params=APIMedianQueryParams(
                median_variable_name='income_g',
                data_fields=('year', 'median_value'),
                table='incomeforecast_county_annual_income_group',
                data_filters=(year_filter,),
                aggregations=(),
                groupby=('year',),
            )
        )

        df_sorted = df.sort_values(by='YEAR', ascending=True)
        assert all(x == y for x, y in zip(
            df_sorted['YEAR'].values, [x for x in range(2013, 2019)]))

    def test_mean_query(self):
        df = self.submit_query(
            query_params=APIMeanQueryParams(
                table='networth_county_annual_net_worth_age_mean',
                data_fields=('year', 'age_g_bottom_coded', 'mean_value'),
                data_filters=(self.year_filter, self.age_filter),
                aggregations=(),
                groupby=('year', 'age_g_bottom_coded'),
                mean_variable_name='net_worth_g',
            )
        )

        assert df['YEAR'].unique() == 2015

    def test_pretty_print(self):
        query_params = APIQueryParams(
            table='geocookbook_county_na_county_metro',
            data_fields=('GEOID5',),
            data_filters=(InFilter(var='cbsa', val=[14454]).to_dict(),),
            aggregations=(),
            groupby=(),
            join=APIQueryParams(
                table='geocookbook_county_na_county_name',
                data_fields=('GEOID5', 'GEOID2', 'GEOID5_NAME'),
                data_filters=(),
                aggregations=(),
                groupby=(),
                on=dict(left=('GEOID5',), right=('GEOID5',)),
                join=APIQueryParams(
                    table='geocookbook_state_na_state_name',
                    data_fields=('GEOID2', 'GEOID2_INIT'),
                    data_filters=(),
                    aggregations=(),
                    groupby=(),
                    on=dict(left=('GEOID2',), right=('GEOID2',)),
                )
            )
        )

        string_form = query_params.pretty_print()
        print(string_form)
        assert isinstance(string_form, str)

        median_query_params = APIMeanQueryParams(
            mean_variable_name='net_worth_g',
            data_fields=('year', 'age_g_bottom_coded', 'mean_value'),
            table='networth_county_annual_net_worth_age_mean',
            data_filters=(self.year_filter, self.age_filter),
            aggregations=(),
            groupby=('year', 'age_g_bottom_coded'),
        )

        string_form = median_query_params.pretty_print()
        print(string_form)
        assert isinstance(string_form, str)

        # Test with different query types at each level
        params = APIGeoJSONQueryParams(
            table='geocookbook_county_na_shapes_full',
            data_fields=({'geoid11': 'geoid_shape'}, 'geometry'),
            data_filters=(),
            aggregations=(),
            groupby=(),
            properties=tuple([
                'geoid11',
                'target_households',
                'median_val',
                'name']),
            join=APIFilterQueryParams(
                data_fields=(),
                table='',
                groupby=(),
                aggregations=(),
                query_type='FILTER',
                data_filters=[GreaterThanOrEqualToFilter(var='target_households', val=100)],
                order=(),
                on=dict(left=('geoid_shape',), right=('geoid11',)),
                inner_query=APICalculationQueryParams(
                    data_fields=[
                        'geoid11',
                        'target_households',
                        'median_val',
                        'name',
                    ],
                    data_filters=(),
                    table='',
                    aggregations=(),
                    groupby=(),
                    inner_query=APIQueryParams(
                        table='incomeforecast_geoid11_annual_income_group',
                        data_fields=('year',
                                     'geoid11',
                                     {'households': 'target_households'}),
                        data_filters=(dict(
                            filter_type='mile_radius_unweighted',
                            filter_value=dict(
                                latitude=42.256922,
                                longitude=-71.040571,
                                miles=3),
                            filter_variable=''),)
                                     + (GreaterThanOrEqualToFilter(var='income_g', val=10).to_dict(),)
                                     + (EqualToFilter(var='year', val=2018).to_dict(),),
                        aggregations=(dict(aggregation_func='sum', variable_name='households'),),
                        groupby=('year', 'geoid11'),
                        join=APIMedianQueryParams(
                            table='incomeforecast_geoid11_annual_income_group',
                            data_fields=({'geoid11': 'geoid_join'},
                                         {'median_value': 'median_val'}),
                            median_variable_name='income_g',
                            data_filters=(EqualToFilter(var='year', val=2018).to_dict(),
                                          dict(
                                              filter_type='mile_radius_unweighted',
                                              filter_value=dict(
                                                  latitude=42.256922,
                                                  longitude=-71.040571,
                                                  miles=3),
                                              filter_variable='')),
                            aggregations=(),
                            groupby=('geoid11',),
                            on=dict(left=('geoid11',), right=('geoid_join',)))))))
        string_form = params.pretty_print()
        print('Test with different query types at each level')
        print(string_form)
        assert isinstance(string_form, str)

        query_params = APIQueryParams(
            table='geocookbook_tract_na_shapes_full',
            data_fields=('GEOID5', 'GEOMETRY', 'NAME'),
            data_filters=(DrivetimeFilter(
                longitude=-96.91386923077042,
                latitude=33.28536026887235,
                minutes=20,
                with_traffic=True),),
            aggregations=(),
            groupby=())

        string_form = query_params.pretty_print()
        print(string_form)
        assert isinstance(string_form, str)

    def test_pretty_print_vba(self):
        query_params = APIQueryParams(
            table='geocookbook_county_na_county_metro',
            data_fields=('GEOID5',),
            data_filters=(InFilter(var='cbsa', val=[14454]).to_dict(),),
            aggregations=(),
            groupby=(),
            order=('GEOID5',),
            join=APIQueryParams(
                table='geocookbook_county_na_county_name',
                data_fields=('GEOID5', 'GEOID2', 'GEOID5_NAME'),
                data_filters=(),
                aggregations=(),
                groupby=(),
                on=dict(left=('GEOID5',), right=('GEOID5',)),
                join=APIQueryParams(
                    table='geocookbook_state_na_state_name',
                    data_fields=('GEOID2', 'GEOID2_INIT'),
                    data_filters=(),
                    aggregations=(),
                    groupby=(),
                    on=dict(left=('GEOID2',), right=('GEOID2',)),
                )
            )
        )

        string_form = query_params.pretty_print_vba()
        print(string_form)
        assert isinstance(string_form, str)

        median_query_params = APIMeanQueryParams(
            mean_variable_name='net_worth_g',
            data_fields=('year', 'age_g_bottom_coded', 'mean_value'),
            table='networth_county_annual_net_worth_age_mean',
            data_filters=(self.year_filter, self.age_filter),
            aggregations=(),
            groupby=('year', 'age_g_bottom_coded'),
        )

        string_form = median_query_params.pretty_print_vba()
        print(string_form)
        self.assertIsInstance(string_form, str)

        query_params = APIQueryParams(
            table='geocookbook_tract_na_shapes_full',
            data_fields=('GEOID5', 'GEOMETRY', 'NAME'),
            data_filters=(DrivetimeFilter(
                longitude=-96.91386923077042,
                latitude=33.28536026887235,
                minutes=20,
                with_traffic=True),),
            aggregations=(),
            groupby=())

        string_form = query_params.pretty_print_vba()
        print(string_form)
        assert isinstance(string_form, str)

    def test_pretty_print_r(self):
        query_params = APIQueryParams(
            table='populationforecast_county_annual_population_age_race_ext',
            data_fields=({'custom:GEOID': 1}, 'YEAR', {'population': 'units'}),
            data_filters=({'filter_type': 'in', 'filter_value': [1, 2, 3, 4, 5, 6, 7],
                           'filter_variable': 'RACE_HISP'},
                          {'filter_type': 'in', 'filter_value': [25025],
                           'filter_variable': 'GEOID5'},
                          {'filter_type': 'between', 'filter_value': [5, 18],
                           'filter_variable': 'AGE_G'}, {'filter_type': 'in',
                                                         'filter_value': [25025, 25027, 36001,
                                                                          20173, 6037, 25021, 6059,
                                                                          6075, 25023, 48453,
                                                                          44001],
                                                         'filter_variable': 'GEOID5'},
                          {'filter_type': 'in', 'filter_value': [2019, 2024, 2025],
                           'filter_variable': 'YEAR'}),
            query_type='COUNT',
            aggregations=({'aggregation_func': 'sum', 'variable_name': 'population'},),
            groupby=('YEAR', 'GEOID'),
            join=APIQueryParams(
                table='geocookbook_county_na_shapes_full',
                data_fields=({'custom:GEOID': 1}, 'area'),
                data_filters=(
                    {'filter_type': 'in', 'filter_value': [25025], 'filter_variable': 'GEOID5'},),
                query_type='AREA',
                aggregations=(),
                groupby=('GEOID',),
                on={'left': ('GEOID',), 'right': ('GEOID',)},
            )
        )

        string_form = query_params.pretty_print_r()
        print(string_form)
        assert isinstance(string_form, str)

        median_query_params = APIMeanQueryParams(
            mean_variable_name='net_worth_g',
            data_fields=('year', 'age_g_bottom_coded', {'mean_value': 'mean_net_worth'}),
            table='networth_county_annual_net_worth_age_mean',
            data_filters=(self.year_filter, self.age_filter),
            aggregations=(),
            groupby=('year', 'age_g_bottom_coded'),
            order=('year', 'age_g_bottom_coded'),
        )

        string_form = median_query_params.pretty_print_r()
        print(string_form)
        self.assertIsInstance(string_form, str)

        query_params = APIQueryParams(
            table='geocookbook_tract_na_shapes_full',
            data_fields=('GEOID5', 'GEOMETRY', 'NAME'),
            data_filters=(DrivetimeFilter(
                longitude=-96.91386923077042,
                latitude=33.28536026887235,
                minutes=20,
                with_traffic=True),),
            aggregations=(),
            groupby=())

        string_form = query_params.pretty_print_r()
        print(string_form)
        assert isinstance(string_form, str)

    def test_calculation_query(self):
        df = self.submit_query(
            query_params=APICalculationQueryParams(
                data_fields=(
                    {'calculate:pop_diff': 'current_pop - past_pop'},
                    'current_pop',
                    'past_pop'),
                data_filters=(),
                table='',
                inner_query=APIQueryParams(
                    table='populationforecast_us_annual_population',
                    data_fields=({'custom:joiner': 1}, {'population': 'current_pop'}),
                    data_filters=(EqualToFilter(var='year', val=2019).to_dict(),),
                    aggregations=(),
                    groupby=(),
                    join=APIQueryParams(
                        table='populationforecast_us_annual_population',
                        data_fields=({'custom:joiner_b': 1}, {'population': 'past_pop'}),
                        data_filters=(EqualToFilter(var='year', val=2018).to_dict(),),
                        aggregations=(),
                        groupby=(),
                        on=dict(left=('joiner',), right=('joiner_b',))
                    )
                ),
                aggregations=(),
                groupby=()))

        diff = df['CURRENT_POP'].sub(df['PAST_POP']).iloc[0].round(3)
        assert df['POP_DIFF'].iloc[0].round(3) == diff

    def test_filter_query(self):
        df = self.submit_query(
            query_params=APIFilterQueryParams(
                data_fields=(),
                data_filters=(GreaterThanOrEqualToFilter(var='population', val=1).to_dict(),),
                table='',
                inner_query=APIQueryParams(
                    table='populationforecast_us_annual_population',
                    data_fields=({'custom:joiner': 1}, 'population'),
                    data_filters=(self.year_filter,),
                    aggregations=(),
                    groupby=(),
                ),
                aggregations=(),
                groupby=()))

        assert len(df) == 1

    def test_filter_pretty_print(self):
        query_params = APIFilterQueryParams(
            data_fields=(),
            data_filters=(GreaterThanOrEqualToFilter(var='population', val=1).to_dict(),),
            table='',
            inner_query=APIQueryParams(
                table='populationforecast_us_annual_population',
                data_fields=({'custom:joiner': 1}, 'population'),
                data_filters=(self.year_filter,),
                aggregations=(),
                groupby=(),
            ),
            aggregations=(),
            groupby=())

        string_form = query_params.pretty_print()
        print(string_form)
        assert isinstance(string_form, str)

    def test_filter_pretty_print_vba(self):
        query_params = APIFilterQueryParams(
            data_fields=(),
            data_filters=(GreaterThanOrEqualToFilter(var='population', val=1).to_dict(),),
            table='',
            inner_query=APIQueryParams(
                table='populationforecast_us_annual_population',
                data_fields=({'custom:joiner': 1}, 'population'),
                data_filters=(self.year_filter,),
                aggregations=(),
                groupby=(),
            ),
            aggregations=(),
            groupby=())

        string_form = query_params.pretty_print_vba()
        print(string_form)
        assert isinstance(string_form, str)

    def test_filter_pretty_print_r(self):
        query_params = APIFilterQueryParams(
            data_fields=(),
            data_filters=(GreaterThanOrEqualToFilter(var='population', val=1).to_dict(),),
            table='',
            inner_query=APIQueryParams(
                table='populationforecast_us_annual_population',
                data_fields=({'custom:joiner': 1}, 'population'),
                data_filters=(self.year_filter,),
                aggregations=(),
                groupby=(),
            ),
            aggregations=(),
            groupby=())

        string_form = query_params.pretty_print_r()
        print(string_form)
        assert isinstance(string_form, str)

    def test_intersects_filter(self):
        df = SDAPIQuery.query_api_df(
            APIQueryParams(
                table='populationforecast_tract_annual_population',
                data_filters=(
                    IntersectsFilter(
                        var='geoid11',
                        val={"type": "Polygon",
                             "coordinates": [
                                 [[-71.17801666259767, 42.43321295705304],
                                  [-71.0145950317383, 42.43321295705304],
                                  [-71.0145950317383, 42.3145122534915],
                                  [-71.17801666259767, 42.3145122534915],
                                  [-71.17801666259767, 42.43321295705304]]]}).to_dict(),
                    EqualToFilter(var='year', val=2019).to_dict()),
                data_fields=('geoid11', 'population'),
                groupby=(),
                aggregations=(),
            ))

        assert len(df.columns) == 2, df.columns
        assert len(df['GEOID11']) == 252, df

    def test_intersects_weighted_filter(self):
        df = SDAPIQuery.query_api_df(
            APIQueryParams(
                table='populationforecast_tract_annual_population',
                data_filters=(
                    IntersectsFilter(
                        detailed_type='intersects_weighted',
                        var='geoid11',
                        val={"type": "Polygon",
                             "coordinates": [
                                 [[-71.17801666259767, 42.43321295705304],
                                  [-71.0145950317383, 42.43321295705304],
                                  [-71.0145950317383, 42.3145122534915],
                                  [-71.17801666259767, 42.3145122534915],
                                  [-71.17801666259767, 42.43321295705304]]]}).to_dict(),
                    BetweenFilter(var='year', val=[2010, 2019]).to_dict()),
                data_fields=('year', 'population'),
                groupby=('year',),
                order=('year',),
                aggregations=(SumAggregation('population'),),
            ))

        self.assertEqual(len(df.columns), 2, df.columns)
        self.assertEqual(len(df), 10)
        self.assertEqual(list(range(2010, 2020)), df['YEAR'].values.tolist())

        df = SDAPIQuery.query_api_df(
            APIMedianQueryParams(
                table='incomeforecast_tract_annual_income_group',
                data_filters=(
                    IntersectsFilter(
                        detailed_type='intersects_weighted',
                        var='geoid11',
                        val={"type": "Polygon",
                             "coordinates": [
                                 [[-71.17801666259767, 42.43321295705304],
                                  [-71.0145950317383, 42.43321295705304],
                                  [-71.0145950317383, 42.3145122534915],
                                  [-71.17801666259767, 42.3145122534915],
                                  [-71.17801666259767, 42.43321295705304]]]}).to_dict(),
                    BetweenFilter(var='year', val=[2010, 2019]).to_dict()),
                data_fields=('year', 'median_value'),
                groupby=('year',),
                order=('year',),
                median_variable_name='income_g',
                aggregations=(),
            ))

        self.assertEqual(len(df.columns), 2, df.columns)
        self.assertEqual(len(df), 10)
        self.assertEqual(list(range(2010, 2020)), df['YEAR'].values.tolist())
        self.assertTrue(df['MEDIAN_VALUE'].gt(0).all())

    def test_overlaps_filter(self):
        import json
        df = SDAPIQuery.query_api_df(
            query_params=APIQueryParams(
                table='userupload_1_785b538b2dd64b67a0fcbab710f3',
                data_fields=('c_name', 'c_street_address'),
                data_filters=(OverlapsMileRadiusFilter(
                    var='geometry',
                    longitude=-96.91386923077042,
                    latitude=33.28536026887235,
                    miles=20),),
                aggregations=(),
                groupby=()))

        assert len(df.columns) == 2, df.columns
        assert len(df['C_NAME']) == 82, df

        df = SDAPIQuery.query_api_df(
            query_params=APIQueryParams(
                table='userupload_1_785b538b2dd64b67a0fcbab710f3',
                data_fields=('c_name', 'c_street_address'),
                data_filters=(OverlapsDrivetimeFilter(
                    var='geometry',
                    longitude=-96.91386923077042,
                    latitude=33.28536026887235,
                    minutes=20),),
                aggregations=(),
                groupby=()))

        assert len(df.columns) == 2, df.columns
        assert len(df['C_NAME']) == 2, df

        df = SDAPIQuery.query_api_df(
            query_params=APIQueryParams(
                table='userupload_1_785b538b2dd64b67a0fcbab710f3',
                data_fields=('c_name', 'c_street_address'),
                data_filters=(OverlapsWalktimeFilter(
                    var='geometry',
                    longitude=-96.84885501,
                    latitude=33.16587,
                    minutes=20),),
                aggregations=(),
                groupby=()))

        assert len(df.columns) == 2, df.columns
        assert len(df['C_NAME']) == 2, df

    def test_pure_shape_query(self):
        df = self.submit_query(
            query_params=APIPureShapeQueryParams(
                table='',
                data_fields=(),
                data_filters=(dict(
                    filter_variable='',
                    filter_type='mile_radius',
                    filter_value=dict(
                        latitude=42.256922,
                        longitude=-71.040571,
                        miles=3)),),
                aggregations=(),
                properties=(),
                groupby=()))
        assert 'geometry' in df['FEATURES'][0][0]

    def test_pure_shape_union_query(self):
        df = self.submit_query(
            query_params=APIPureShapeUnionQueryParams(
                table='',
                data_fields=(),
                data_filters=(),
                aggregations=(),
                properties=(),
                groupby=(),
                join=[
                    APIPureShapeQueryParams(
                        table='',
                        data_fields=(),
                        data_filters=(dict(
                            filter_variable='',
                            filter_type='mile_radius',
                            filter_value=dict(
                                latitude=42.256922,
                                longitude=-71.040571,
                                miles=3)),),
                        aggregations=(),
                        properties=(),
                        groupby=()),
                    APIPureShapeQueryParams(
                        table='',
                        data_fields=(),
                        data_filters=(dict(
                            filter_variable='',
                            filter_type='mile_radius',
                            filter_value=dict(
                                latitude=42.256922,
                                longitude=-71.040571,
                                miles=5)),),
                        aggregations=(),
                        properties=(),
                        groupby=())
                ]))
        assert 'geometry' in df['FEATURES'][0][0]
        assert len(df['FEATURES'][0]) == 2

    def test_miles_distance_query(self):
        df = self.submit_query(
            query_params=APIMilesDistanceQueryParams(
                start_latitude=41.82937349570897,
                start_longitude=-71.41338050365448,
                end_latitude=42.35339843570063,
                end_longitude=-71.06788516044617))
        assert 'DISTANCE' in df
        assert round(df['DISTANCE'][0], 6) == round(40.3163963879, 6), df['DISTANCE'][0]

    def test_driving_distance_query(self):
        df = self.submit_query(
            query_params=APIDrivingDistanceQueryParams(
                start_latitude=41.82937349570897,
                start_longitude=-71.41338050365448,
                end_latitude=42.35339843570063,
                end_longitude=-71.06788516044617))
        assert 'DISTANCE' in df
        assert round(df['DISTANCE'][0], 4) == round(44.96875, 4), df['DISTANCE'][0]
        assert 'TIME' in df
        assert round(df['TIME'][0], 6) == round(60.0833333333, 6), df['TIME'][0]

        df = self.submit_query(
            query_params=APIDrivingDistanceQueryParams(
                traffic=True,
                start_latitude=41.82937349570897,
                start_longitude=-71.41338050365448,
                end_latitude=42.35339843570063,
                end_longitude=-71.06788516044617))
        assert 'DISTANCE' in df
        assert round(df['DISTANCE'][0], 4) == round(44.96875, 4), df['DISTANCE'][0]
        assert 'TIME' in df
        assert round(df['TIME'][0], 6) == round(55.7333333333, 6), df['TIME'][0]

    def test_walking_distance_query(self):
        df = self.submit_query(
            query_params=APIWalkingDistanceQueryParams(
                start_latitude=41.82937349570897,
                start_longitude=-71.41338050365448,
                end_latitude=41.8222540665299,
                end_longitude=-71.41181409358978))
        assert 'DISTANCE' in df
        assert round(df['DISTANCE'][0], 6) == round(0.5761363636, 6), df['DISTANCE'][0]
        assert 'TIME' in df
        assert round(df['TIME'][0], 6) == round(17.4333333333, 6), df['TIME'][0]
