# Sample queries

## Population density in the Boston, MA MSA

> Population density in Boston up to 2015:

```python
from strato_query import SDAPIQuery, APIQueryParams, EqualToFilter, LessThanFilter

df = SDAPIQuery.query_api_df(
    query_params=APIQueryParams(
        query_type='COUNT',
        table='populationforecast_metro_annual_population',
        data_fields=('year', 'cbsa', {'population': 'population'}),
        data_filters=(
            LessThanFilter(var='year', val=2015).to_dict(),
            EqualToFilter(var='cbsa', val=14454).to_dict(),
        ),
        aggregations=(dict(aggregation_func='sum', variable_name='population'),),
        groupby=('cbsa', 'year'),
        order=('year',),
        join=APIQueryParams(
            query_type='AREA',
            table='geocookbook_metro_na_shapes_full',
            data_fields=('cbsa', 'area', 'name'),
            data_filters=(EqualToFilter(var='cbsa', val=14454).to_dict(),),
            groupby=('cbsa', 'name'),
            aggregations=(),
            on=dict(left=('cbsa',), right=('cbsa',)),
        )
    )
)
```

```r
library(stRatoquery)

apiToken = 'my-api-token'

df = submit_api_query(
  query = api_query_params(
    table = 'populationforecast_metro_annual_population',
    data_fields = api_fields(fields_list = list('year', 'cbsa', list(population = 'population'))),
    data_filters = list(
        lt_filter(filter_variable = 'year', filter_value = 2015),
        eq_filter(filter_variable = 'cbsa', filter_value = 14454)
    ),
    groupby=c('year', 'cbsa'),
    aggregations = list(sum_aggregation(variable_name = 'population')),
    join = api_query_params(
        table = 'geocookbook_metro_na_shapes_full',
        query_type = 'AREA',
        data_fields = api_fields(fields_list = list('cbsa', 'area', 'name')),
        data_filters = list(),
        groupby = c('cbsa', 'name'),
        aggregations = list(),
        on = list(left = c('cbsa'), right = c('cbsa'))
    )
  ),
  apiToken = apiToken)

df$pop_per_sq_mi = df$population / df$area
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": { \"query_type\": \"COUNT\", \"data_fields\": [ \"year\", \"cbsa\", { \"population\": \"population\" } ], \"table\": \"populationforecast_metro_annual_population\", \"groupby\": [ \"cbsa\", \"year\" ], \"data_filters\": [ { \"filter_type\": \"lt\", \"filter_value\": 2015, \"filter_variable\": \"year\" }, { \"filter_type\": \"eq\", \"filter_value\": 14454, \"filter_variable\": \"cbsa\" } ], \"aggregations\": [ { \"aggregation_func\": \"sum\", \"variable_name\": \"population\" } ], \"join\": { \"query_type\": \"AREA\", \"data_fields\": [ \"cbsa\", \"area\", \"name\" ], \"table\": \"geocookbook_metro_na_shapes_full\", \"groupby\": [ \"cbsa\", \"name\" ], \"data_filters\": [ { \"filter_type\": \"eq\", \"filter_value\": 14454, \"filter_variable\": \"cbsa\" } ], \"aggregations\": [], \"on\": { \"left\": [ \"cbsa\" ], \"right\": [ \"cbsa\" ] } }, \"order\": [ \"year\" ]}}"
```

Calculating the population density (population per square mile) in the Boston, MA MSA, by year.

|YEAR|NAME|POP_PER_SQ_MI|
|----|----|-------------|
|2014|Boston, MA|1665.827530|
|2013|Boston, MA|1651.187549|
|2012|Boston, MA|1633.847778|
|2011|Boston, MA|1617.340007|
|2010|Boston, MA|1601.802067|

## Population within five miles of latitude-longitude pair

> Population within five miles of 40.7589542, -73.9937348'):

```python
from strato_query import SDAPIQuery, APIQueryParams, MileRadiusFilter, BetweenFilter

df = SDAPIQuery.query_api_df(
    query_params=APIQueryParams(
        table='populationforecast_tract_annual_population',
        data_fields=('YEAR', {'population': 'population_within_5_miles'}),
        data_filters=(
            # Aggregate data within five miles of 40.7589542, -73.9937348
            MileRadiusFilter(
                latitude=40.75895, longitude=-73.9937, miles=5).to_dict(),
            # Only get data for years between 2010 and 2020 (inclusive)
            BetweenFilter(var='year', val=[2010, 2020]).to_dict()),
        aggregations=({'variable_name': 'population', 'aggregation_func': 'sum'},),
        groupby=('year',)))
```

```r
library(stRatoquery)

apiToken = 'my-api-token'

df = submit_api_query(
  api_query_params(
    table = 'populationforecast_tract_annual_population',
    data_fields = api_fields(fields_list = list('YEAR', list(population = 'population_within_5_miles'))),
    data_filters = list(
      # Aggregate data within five miles of 40.7589, -73.9937
      mile_radius_filter(latitude = 40.7589, longitude = -73.9937, miles = 5),
      # Only get data for years between 2010 and 2020 (inclusive)
      between_filter(filter_variable = 'year', filter_value = c(2010, 2020))),
    aggregations = list(sum_aggregation(variable_name = 'population')),
    groupby = c('year')),
  apiToken = apiToken)
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": { \"query_type\": \"COUNT\", \"data_fields\": [ \"YEAR\", { \"population\": \"population_within_5_miles\" } ], \"table\": \"populationforecast_tract_annual_population\", \"groupby\": [ \"year\" ], \"data_filters\": [ { \"filter_type\": \"mile_radius\", \"filter_value\": { \"latitude\": 40.75895, \"longitude\": -73.9937, \"miles\": 5 }, \"filter_variable\": \"\" }, { \"filter_type\": \"between\", \"filter_value\": [ 2010, 2020 ], \"filter_variable\": \"year\" } ], \"aggregations\": [ { \"variable_name\": \"population\", \"aggregation_func\": \"sum\" } ]}}"
```

Calculating the population within a mile radius buffer, by year.

|YEAR|POPULATION_WITHIN_5_MILES|
|----|-------------------------|
|2010|2.333544e+06|
|2011|2.369469e+06|
|2012|2.400245e+06|
|2013|2.420539e+06|
|2014|2.438206e+06|
