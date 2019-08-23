# Query types

## Simple queries

> This query returns households by age, income group, and year for all census tracts in Massachusetts starting in 2010

```python
from strato_query import SDAPIQuery, APIQueryParams
from strato_query.filters import EqualToFilter, GreaterThanOrEqualToFilter

SDAPIQuery.query_api_df(
    APIQueryParams(
        data_fields=('year', 'geoid11', 'age_g', 'income_g', 'households'),
        table='incomeforecast_tract_annual_income_group_age',
        data_filters=[
            EqualToFilter('geoid2', 25),
            GreaterThanOrEqualToFilter('year', 2010),
        ],
        aggregations=(),
        groupby=()))
```

```r
library(stRatoquery)

df = submit_api_query(
  query = api_query_params(
    table = 'incomeforecast_tract_annual_income_group_age',
    data_fields = api_fields(fields_list = list('year', 'geoid11', 'age_g', 'income_g', 'households')),
    data_filters = list(
        eq_filter(filter_variable = 'geoid2', filter_value = 25),
        ge_filter(filter_variable = 'year', filter_value = 2010)
    ),
    aggregations=list(),
    groupby=list()
  ),
  apiToken = apiToken)
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": { \"query_type\": \"COUNT\", \"data_fields\": [ \"year\", \"geoid11\", \"age_g\", \"income_g\", \"households\" ], \"table\": \"incomeforecast_tract_annual_income_group_age\", \"groupby\": [ ], \"data_filters\": [ { \"filter_type\": \"eq\", \"filter_value\": 25, \"filter_variable\": \"geoid2\" }, { \"filter_type\": \"ge\", \"filter_value\": 2010, \"filter_variable\": \"year\" } ], \"aggregations\": [], \"order\": []}}"
```

```vb
Dim query As Dictionary

Set query = apiQueryParameters( _
    table:="incomeforecast_tract_annual_income_group_age", _
    dataFields:=Array("year", "geoid11", "age_g", "income_g", "households"), _
    dataFilters:=Array( _
        equalToFilter(filterVariable:="geoid2", filterValue:=25), _
        greaterThanOrEqualToFilter(filterVariable:="year", filterValue:=2010)), _
    groupby:=Array(), _
    aggregations:=Array())

' Write the results to "Example Sheet" (note that this sheet will need to exist first)
Call writeToSheet(results:=submitAPIQuery(query), sheetName:="Example Sheet")
```

Basic API queries evaluate like simple `SELECT` statements from the StratoDem Analytics database.

Queries roughly translate into SQL as `SELECT data_fields FROM table WHERE data_filters GROUP BY groupby;`

## Queries with aggregations

> This query returns the number of households age 75+ with at least $50,000 in household income by county and year for each county in California

```python
from strato_query import SDAPIQuery, APIQueryParams
from strato_query.aggregations import SumAggregation
from strato_query.filters import EqualToFilter, GreaterThanOrEqualToFilter

SDAPIQuery.query_api_df(
    APIQueryParams(
        # Passing in a dictionary to data_fields allows for renaming variables in the resulting DataFrame or JSON
        data_fields=['year', 'geoid5', {'households': 'households_age_75plus_hhi_50k_plus'}],
        table='incomeforecast_county_annual_income_group_age',
        data_filters=(
            EqualToFilter('geoid2', 6),
            # Cutoff for age 75+
            GreaterThanOrEqualToFilter('age_g', 16),
            # Cutoff for $50,000+ HHI
            GreaterThanOrEqualToFilter('income_g', 10),
        ),
        groupby=('year', 'geoid5'),
        aggregations=[SumAggregation('households')],
        order=('year', 'geoid5')
    ))
```

```r
library(stRatoquery)

df = submit_api_query(
  query = api_query_params(
    table = 'incomeforecast_county_annual_income_group_age',
    # Passing in a mapping to data_fields allows for renaming variables in the resulting data.frame or JSON
    data_fields = api_fields(fields_list = list('year', 'geoid5', list(households = 'households_age_75plus_50k_plus'))),
    data_filters = list(
        eq_filter(filter_variable = 'geoid2', filter_value = 6),
        # Cutoff for age 75+
        ge_filter(filter_variable = 'age_g', filter_value = 16),
        # Cutoff for $50,000+ HHI
        ge_filter(filter_variable = 'income_g', filter_value = 10)
    ),
    aggregations = list(sum_aggregation(variable_name = 'households')),
    groupby = list('year', 'geoid5'),
    order = list('year', 'geoid5')
  ),
  apiToken = apiToken)
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{\"query_type\": \"COUNT\", \"data_fields\": [\"year\", \"geoid5\", {\"households\": \"households_age_75plus_hhi_50k_plus\"}], \"table\": \"incomeforecast_county_annual_income_group_age\", \"groupby\": [\"year\", \"geoid5\"], \"data_filters\": [{\"filter_type\": \"eq\", \"filter_value\": 6, \"filter_variable\": \"geoid2\"}, {\"filter_type\": \"ge\", \"filter_value\": 16, \"filter_variable\": \"age_g\"}, {\"filter_type\": \"ge\", \"filter_value\": 10, \"filter_variable\": \"income_g\"}], \"aggregations\": [{\"aggregation_func\": \"sum\", \"variable_name\": \"households\"}], \"order\": [\"year\", \"geoid5\"]}"
```

```vb
Dim query As Dictionary

Set query = apiQueryParameters( _
    table:="incomeforecast_county_annual_income_group_age", _
    dataFields:=Array("year", "geoid5", renameVariable(original:="households", renamed:="households_age_75plus_hhi_50k_plus")), _
    dataFilters:=Array( _
        equalToFilter(filterVariable:="geoid2", filterValue:=6), _
        greaterThanOrEqualToFilter(filterVariable:="age_g", filterValue:=16), _
        greaterThanOrEqualToFilter(filterVariable:="inocme_g", filterValue:=10)), _
    groupby:=Array("year", "geoid5"), _
    order:=Array("year", "geoid5"), _
    aggregations:=Array(sumAggregation(variableName:="households")))

' Write the results to "Example Sheet" (note that this sheet will need to exist first)
Call writeToSheet(results:=submitAPIQuery(query), sheetName:="Example Sheet")
```

In many cases, we want to aggregate data returned by the API. For example, if we have the SQL query:
`SELECT year, geoid5, sum(households) FROM incomeforecast_county_annual_income_group_age WHERE income_g >= 5 AND age_g >= 17 GROUP BY year, geoid5 ORDER BY year, geoid5;`, 
we need to group by the `year` and `geoid5` (county) columns, and then get the sum of `households` for each combination.

The `groupby` and `aggregations` arguments tell the API which columns to group on and which aggregations to apply.

## Median queries

> This query returns the median household income for all households by census tract in Suffolk County, MA in 2019

```python
from strato_query import SDAPIQuery, APIMedianQueryParams
from strato_query.filters import EqualToFilter

SDAPIQuery.query_api_df(
    APIMedianQueryParams(
        median_variable_name='income_g',
        table='incomeforecast_tract_annual_income_group',
        data_fields=('year', 'geoid11', 'median_value'),
        data_filters=[
            EqualToFilter('year', 2019),
            EqualToFilter('geoid5', 25025),
        ],
        aggregations=(),
        groupby=('year', 'geoid11')       
    ))
```

```r
library(stRatoquery)

df = submit_api_query(
  query = median_query_params(
    table = 'incomeforecast_tract_annual_income_group',
    data_fields = api_fields(fields_list = list('year', 'geoid11', 'median_value')),
    data_filters = list(
        eq_filter(filter_variable = 'year', filter_value = 2019),
        eq_filter(filter_variable = 'geoid5', filter_value = 25025)
    ),
    groupby=c('year', 'geoid11'),
    median_variable_name='income_g',
    aggregations=list()
  ),
  apiToken = apiToken)
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    - d "{\"query_type\": \"MEDIAN\", \"data_fields\": [\"year\", \"geoid11\", \"median_value\"], \"table\": \"incomeforecast_tract_annual_income_group\", \"groupby\": [\"year\", \"geoid11\"], \"data_filters\": [{\"filter_type\": \"eq\", \"filter_value\": 2019, \"filter_variable\": \"year\"}, {\"filter_type\": \"eq\", \"filter_value\": 25025, \"filter_variable\": \"geoid5\"}], \"aggregations\": [], \"median_variable_name\": \"income_g\"}"
```

```vb
Dim query As Dictionary

Set query = medianQueryParameters( _
    table:="incomeforecast_tract_annual_income_group", _
    dataFields:=Array("year", "geoid11", "median_value"), _
    dataFilters:=Array(equalToFilter(filterVariable:="year", filterValue:=2019), equalToFilter(filterVariable:="geoid5", filterValue:=25025)), _
    aggregations:=Array(), _
    groupby:=Array("year", "geoid11"), _
    medianVariableName:="income_g")

' Write the results to "Example Sheet" (note that this sheet will need to exist first)
Call writeToSheet(results:=submitAPIQuery(query), sheetName:="Example Sheet")
```

To query median household income, net worth, home values, or other metrics, a special median query is needed.

These queries require a `median_variable_name` argument, which tells the API service which variable to 
use to compute the median value.

## Mean/average queries

> This query returns the median household income for all households by census tract in Suffolk County, MA in 2019

```python
from strato_query import SDAPIQuery, APIMeanQueryParams
from strato_query.filters import EqualToFilter

SDAPIQuery.query_api_df(
    APIMeanQueryParams(
        mean_variable_name='income_g',
        table='incomeforecast_tract_annual_income_group',
        data_fields=('year', 'geoid11', 'mean_value'),
        data_filters=[
            EqualToFilter('year', 2019),
            EqualToFilter('geoid5', 25025),
        ],
        aggregations=(),
        groupby=('year', 'geoid11')       
    ))
```

```r
library(stRatoquery)

df = submit_api_query(
  query = mean_query_params(
    table = 'incomeforecast_tract_annual_income_group',
    data_fields = api_fields(fields_list = list('year', 'geoid11', 'mean_value')),
    data_filters = list(
        eq_filter(filter_variable = 'year', filter_value = 2019),
        eq_filter(filter_variable = 'geoid5', filter_value = 25025)
    ),
    groupby = c('year', 'geoid11'),
    mean_variable_name = 'income_g',
    aggregations = list()
  ),
  apiToken = apiToken)
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    - d "{\"query_type\": \"MEAN\", \"data_fields\": [\"year\", \"geoid11\", \"mean_value\"], \"table\": \"incomeforecast_tract_annual_income_group\", \"groupby\": [\"year\", \"geoid11\"], \"data_filters\": [{\"filter_type\": \"eq\", \"filter_value\": 2019, \"filter_variable\": \"year\"}, {\"filter_type\": \"eq\", \"filter_value\": 25025, \"filter_variable\": \"geoid5\"}], \"aggregations\": [], \"mean_variable_name\": \"income_g\"}"
```

```vb
Dim query As Dictionary

Set query = meanQueryParameters( _
    table:="incomeforecast_tract_annual_income_group", _
    dataFields:=Array("year", "geoid11", "mean_value"), _
    dataFilters:=Array(equalToFilter(filterVariable:="year", filterValue:=2019), equalToFilter(filterVariable:="geoid5", filterValue:=25025)), _
    aggregations:=Array(), _
    groupby:=Array("year", "geoid11"), _
    meanVariableName:="income_g")

' Write the results to "Example Sheet" (note that this sheet will need to exist first)
Call writeToSheet(results:=submitAPIQuery(query), sheetName:="Example Sheet")
```

To query mean household income, net worth, home values, or other metrics, a special mean query is needed.

These queries require a `mean_variable_name` argument, which tells the API service which variable to 
use to compute the mean value.

## GeoJSON queries

## Combining queries
