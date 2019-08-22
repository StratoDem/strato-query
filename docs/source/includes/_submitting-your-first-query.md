# Submitting your first query

> Finds median household income in the US for those 80+ from 2010 to 2013

```python
from strato_query import SDAPIQuery, APIMedianQueryParams, GreaterThanOrEqualToFilter, BetweenFilter

df = SDAPIQuery.query_api_df(
    query_params=APIMedianQueryParams(
        query_type='MEDIAN',
        table='incomeforecast_us_annual_income_group_age',
        data_fields=('year', {'median_value': 'median_income'}),
        median_variable_name='income_g',
        data_filters=(
            GreaterThanOrEqualToFilter(var='age_g', val=17),
            BetweenFilter(var='year', val=[2010, 2013]),
        ),
        groupby=('year',),
        order=('year',),
        aggregations=(),
    )
)
```

```r
library(stRatoquery)
apiToken = 'my-api-token'

df = submit_api_query(
  query = median_query_params(
    table = 'incomeforecast_us_annual_income_group_age',
    data_fields = api_fields(fields_list = list('year', list(median_value = 'median_hhi'))),
    data_filters = list(
        ge_filter(filter_variable = 'age_g', filter_value = 17),
        between_filter(filter_variable = 'year', filter_value = c(2010, 2013))
    ),
    groupby=c('year'),
    median_variable_name='income_g',
    aggregations=list()
  ),
  apiToken = apiToken)
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": { \"query_type\": \"MEDIAN\", \"data_fields\": [ \"year\", { \"median_value\": \"median_income\" } ], \"table\": \"incomeforecast_us_annual_income_group_age\", \"groupby\": [ \"year\" ], \"data_filters\": [ { \"filter_type\": \"ge\", \"filter_value\": 17, \"filter_variable\": \"age_g\" }, { \"filter_type\": \"between\", \"filter_value\": [ 2010, 2013 ], \"filter_variable\": \"year\" } ], \"aggregations\": [], \"order\": [ \"year\" ], \"median_variable_name\": \"income_g\"}}"
```

A basic query to the StratoDem Analytics API submits query parameters with authentication via the API token.
