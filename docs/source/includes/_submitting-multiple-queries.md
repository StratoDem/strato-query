# Submitting multiple queries

> Submit multiple queries with unique IDs to the API for a batch query

```python
from strato_query import SDAPIQuery, APIQueryParams

# This returns a dictionary with the query ID pointing to a pandas.DataFrame
SDAPIQuery.query_api_multiple(
    queries={
        'query1': APIQueryParams(
            table='populationforecast_us_annual_population',
            data_fields=('year', 'population'),
            data_filters=(),
            groupby=(),
            aggregations=()),
        'query2': APIQueryParams(
            table='populationforecast_state_annual_population_age',
            data_fields=('year', 'geoid2', 'age_g', 'population'),
            data_filters=(),
            groupby=(),
            aggregations=()),
    })
```

```r
# Not officially supported
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"queries\": {\"query1\": { \"query_type\": \"COUNT\", \"data_fields\": [ \"year\", \"cbsa\", { \"population\": \"population\" } ], \"table\": \"populationforecast_metro_annual_population\", \"groupby\": [ \"cbsa\", \"year\" ], \"data_filters\": [ { \"filter_type\": \"lt\", \"filter_value\": 2015, \"filter_variable\": \"year\" }, { \"filter_type\": \"eq\", \"filter_value\": 14454, \"filter_variable\": \"cbsa\" } ], \"aggregations\": [ { \"aggregation_func\": \"sum\", \"variable_name\": \"population\" } ], \"join\": { \"query_type\": \"AREA\", \"data_fields\": [ \"cbsa\", \"area\", \"name\" ], \"table\": \"geocookbook_metro_na_shapes_full\", \"groupby\": [ \"cbsa\", \"name\" ], \"data_filters\": [ { \"filter_type\": \"eq\", \"filter_value\": 14454, \"filter_variable\": \"cbsa\" } ], \"aggregations\": [], \"on\": { \"left\": [ \"cbsa\" ], \"right\": [ \"cbsa\" ] } }, \"order\": [ \"year\" ]}}, \"query2\": { \"query_type\": \"COUNT\", \"data_fields\": [ \"year\", \"cbsa\", { \"population\": \"population\" } ], \"table\": \"populationforecast_metro_annual_population\", \"groupby\": [ \"cbsa\", \"year\" ], \"data_filters\": [ { \"filter_type\": \"lt\", \"filter_value\": 2015, \"filter_variable\": \"year\" }, { \"filter_type\": \"eq\", \"filter_value\": 14454, \"filter_variable\": \"cbsa\" } ], \"aggregations\": [ { \"aggregation_func\": \"sum\", \"variable_name\": \"population\" } ], \"join\": { \"query_type\": \"AREA\", \"data_fields\": [ \"cbsa\", \"area\", \"name\" ], \"table\": \"geocookbook_metro_na_shapes_full\", \"groupby\": [ \"cbsa\", \"name\" ], \"data_filters\": [ { \"filter_type\": \"eq\", \"filter_value\": 14454, \"filter_variable\": \"cbsa\" } ], \"aggregations\": [], \"on\": { \"left\": [ \"cbsa\" ], \"right\": [ \"cbsa\" ] } }, \"order\": [ \"year\" ]}}}}"
```

```vb
' Not officially supported
```

The StratoDem Analytics API supports batches of queries to execute in parallel. The Python package supports this 
through the `SDAPIQuery.query_api_multiple` method, which takes a dictionary of queries and returns a dictionary of `pandas.DataFrames`
