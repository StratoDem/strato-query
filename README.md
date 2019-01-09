# Strato-Query
tools to help create queries to StratoDem's API

## Installation and usage
`$ pip install strato-query`

### Authentication
`strato_query` looks for an `API_TOKEN` environment variable.
```bash
# Example passing a StratoDem Analytics API token to a Python file using the API
$ API_TOKEN=my-api-token-here python examples/examples.py
```

### Example use of query base class with API call and example filter
```python
from strato_query.base_API_query import *
from strato_query.standard_filters import *


class ExampleAPIQuery(BaseAPIQuery):
    @classmethod
    def get_df_from_API_call(cls, **kwargs):
        # This API call will return the population 65+ in 2018 within 5 miles of the lat/long pair
        age_filter = GtrThanOrEqFilter(
            var='age_g',
            val=14).to_dict()

        year_filter = EqFilter(
            var='year',
            val=2018).to_dict()

        mile_radius_filter = dict(
            filter_type='mile_radius',
            filter_value=dict(
                latitude=26.606484,
                longitude=-81.851531,
                miles=5),
            filter_variable='')

        df = cls.query_api_df(
            query_params=APIQueryParams(
                table='populationforecast_tract_annual_population_age',
                data_fields=('POPULATION',),
                data_filters=(age_filter, year_filter, mile_radius_filter),
                query_type='COUNT',
                aggregations=(),
                groupby=()
            )
        )

        return df
```

### Median household income for 80+ households across the US, by year
```python
from strato_query.base_API_query import *
from strato_query.standard_filters import *


# Finds median household income in the US for those 80+ from 2010 to 2013
df = BaseAPIQuery.query_api_df(
    query_params=APIMedianQueryParams(
        query_type='MEDIAN',
        table='incomeforecast_us_annual_income_group_age',
        data_fields=('year', {'median_value': 'median_income'}),
        median_variable_name='income_g',
        data_filters=(
            GtrThanOrEqFilter(var='age_g', val=17).to_dict(),
            BetweenFilter(var='year', val=[2010, 2013]).to_dict(),
        ),
        groupby=('year',),
        order=('year',),
        aggregations=(),
    )
)

print('Median US household income 80+:')
print(df.head())
```

Output:
```
Median US household income 80+:
   MEDIAN_VALUE  YEAR
0         27645  2010
1         29269  2011
2         30474  2012
3         30712  2013
```