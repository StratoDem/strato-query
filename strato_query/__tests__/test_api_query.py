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
