"""
StratoDem Analytics : test_api_query
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

December 26, 2018
"""

import unittest

from strato_query.base_API_query import *
from strato_query.standard_filters import *


class TestAPIQuery(unittest.TestCase, BaseAPIQuery):
    @classmethod
    def test_query_call(cls):
        age_filter = EqFilter(
            var='age_g',
            val=18).to_dict()

        year_filter = BetweenFilter(
            var='year',
            val=[2013, 2018]).to_dict()

        df = cls.submit_query(
            query_params=APIQueryParams(
                query_type='COUNT',
                data_fields=('year', 'population'),
                table='populationforecast_us_annual_population_age',
                data_filters=(age_filter, year_filter),
                aggregations=(dict(aggregation_func='sum',
                                   variable_name='population'),),
                groupby=('year',),
            )
        )

        df_sorted = df.sort_values(by='YEAR', ascending=True)
        assert all(x == y for x, y in zip(
            df_sorted['YEAR'].values, [x for x in range(2013, 2019)]))

    @classmethod
    def test_multi_join(cls):
        df = cls.query_api_df(
            query_params=APIQueryParams(
                table='geocookbook_county_na_county_metro',
                data_fields=('GEOID5',),
                data_filters=(InFilter(var='cbsa', val=[14454]).to_dict(),),
                query_type='COUNT',
                aggregations=(),
                groupby=(),
                join=APIQueryParams(
                    table='geocookbook_county_na_county_name',
                    data_fields=('GEOID5', 'GEOID2', 'GEOID5_NAME'),
                    data_filters=(),
                    query_type='COUNT',
                    aggregations=(),
                    groupby=(),
                    on=dict(left=('GEOID5',), right=('GEOID5',)),
                    join=APIQueryParams(
                        table='geocookbook_state_na_state_name',
                        data_fields=('GEOID2', 'GEOID2_INIT'),
                        data_filters=(),
                        query_type='COUNT',
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
