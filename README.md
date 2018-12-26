# Strato-Query
tools to help create queries to StratoDem's API

## Installation and usage
`$ pip install strato-query`


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
