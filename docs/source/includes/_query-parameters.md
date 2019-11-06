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
    -d "{ \"token\": \"my-api-token\", \"query\": {\"query_type\": \"COUNT\", \"data_fields\": [\"year\", \"geoid5\", {\"households\": \"households_age_75plus_hhi_50k_plus\"}], \"table\": \"incomeforecast_county_annual_income_group_age\", \"groupby\": [\"year\", \"geoid5\"], \"data_filters\": [{\"filter_type\": \"eq\", \"filter_value\": 6, \"filter_variable\": \"geoid2\"}, {\"filter_type\": \"ge\", \"filter_value\": 16, \"filter_variable\": \"age_g\"}, {\"filter_type\": \"ge\", \"filter_value\": 10, \"filter_variable\": \"income_g\"}], \"aggregations\": [{\"aggregation_func\": \"sum\", \"variable_name\": \"households\"}], \"order\": [\"year\", \"geoid5\"]}}"
```

```vb
Dim query As Dictionary

Set query = apiQueryParameters( _
    table:="incomeforecast_county_annual_income_group_age", _
    dataFields:=Array("year", "geoid5", renameVariable(original:="households", renamed:="households_age_75plus_hhi_50k_plus")), _
    dataFilters:=Array( _
        equalToFilter(filterVariable:="geoid2", filterValue:=6), _
        greaterThanOrEqualToFilter(filterVariable:="age_g", filterValue:=16), _
        greaterThanOrEqualToFilter(filterVariable:="income_g", filterValue:=10)), _
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
    -d "{ \"token\": \"my-api-token\", \"query\": {\"query_type\": \"MEDIAN\", \"data_fields\": [\"year\", \"geoid11\", \"median_value\"], \"table\": \"incomeforecast_tract_annual_income_group\", \"groupby\": [\"year\", \"geoid11\"], \"data_filters\": [{\"filter_type\": \"eq\", \"filter_value\": 2019, \"filter_variable\": \"year\"}, {\"filter_type\": \"eq\", \"filter_value\": 25025, \"filter_variable\": \"geoid5\"}], \"aggregations\": [], \"median_variable_name\": \"income_g\"}}"
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
    -d "{ \"token\": \"my-api-token\", \"query\": {\"query_type\": \"MEAN\", \"data_fields\": [\"year\", \"geoid11\", \"mean_value\"], \"table\": \"incomeforecast_tract_annual_income_group\", \"groupby\": [\"year\", \"geoid11\"], \"data_filters\": [{\"filter_type\": \"eq\", \"filter_value\": 2019, \"filter_variable\": \"year\"}, {\"filter_type\": \"eq\", \"filter_value\": 25025, \"filter_variable\": \"geoid5\"}], \"aggregations\": [], \"mean_variable_name\": \"income_g\"}}"
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

## Combining multiple queries

> This query joins two results on common columns to compute population density

```python
from strato_query import SDAPIQuery, APIQueryParams
from strato_query.filters import EqualToFilter, LessThanFilter

df = SDAPIQuery.query_api_df(
    query_params=APIQueryParams(
        query_type='COUNT',
        table='populationforecast_metro_annual_population',
        data_fields=('year', 'cbsa', {'population': 'population'}),
        data_filters=(
            LessThanFilter(var='year', val=2015),
            EqualToFilter(var='cbsa', val=14454),
        ),
        aggregations=(dict(aggregation_func='sum', variable_name='population'),),
        groupby=('cbsa', 'year'),
        order=('year',),
        join=APIQueryParams(
            query_type='AREA',
            table='geocookbook_metro_na_shapes_full',
            data_fields=('cbsa', 'area', 'name'),
            data_filters=[EqualToFilter(var='cbsa', val=14454)],
            groupby=('cbsa', 'name'),
            aggregations=(),
            on=dict(left=('cbsa',), right=('cbsa',)),
        )
    )
)

df['POP_PER_SQ_MI'] = df['POPULATION'].div(df['AREA'])
df_final = df[['YEAR', 'NAME', 'POP_PER_SQ_MI']]
```

```r
library(stRatoquery)

api_query_params(
  table = 'populationforecast_metro_annual_population',
  data_fields = api_fields(fields_list = list('year', 'cbsa', list('population' = 'population'))),
  data_filters = list(lt_filter(filter_variable = "year", filter_value = 2015), eq_filter(filter_variable = "cbsa", filter_value = 14454)),
  aggregations = list(sum_aggregation(variable_name = "population")),
  groupby = c("cbsa", "year"),
  order = c("year"),
  join = api_query_params(
      table = 'geocookbook_metro_na_shapes_full',
      data_fields = api_fields(fields_list = list('cbsa', 'area', 'name')),
      data_filters = list(eq_filter(filter_variable = "cbsa", filter_value = 14454)),
      aggregations = list(),
      groupby = c("cbsa", "name"),
      on = list(left = c('cbsa'), right = c('cbsa')),
      query_type = "AREA"),
  query_type = "COUNT")
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": {\"query_type\": \"COUNT\", \"data_fields\": [\"year\", \"cbsa\", {\"population\": \"population\"}], \"table\": \"populationforecast_metro_annual_population\", \"groupby\": [\"cbsa\", \"year\"], \"data_filters\": [{\"filter_type\": \"lt\", \"filter_value\": 2015, \"filter_variable\": \"year\"}, {\"filter_type\": \"eq\", \"filter_value\": 14454, \"filter_variable\": \"cbsa\"}], \"aggregations\": [{\"aggregation_func\": \"sum\", \"variable_name\": \"population\"}], \"join\": {\"query_type\": \"AREA\", \"data_fields\": [\"cbsa\", \"area\", \"name\"], \"table\": \"geocookbook_metro_na_shapes_full\", \"groupby\": [\"cbsa\", \"name\"], \"data_filters\": [{\"filter_type\": \"eq\", \"filter_value\": 14454, \"filter_variable\": \"cbsa\"}], \"aggregations\": [], \"on\": {\"left\": [\"cbsa\"], \"right\": [\"cbsa\"]}}, \"order\": [\"year\"]}}"
```

```vb
apiQueryParameters( _
    table:="populationforecast_metro_annual_population", _
    dataFields:=Array("year", "cbsa", renameVariable(original:="population", renamed:="population")), _
    dataFilters:=Array(lessThanFilter(filterVariable:="year", filterValue:=2015), equalToFilter(filterVariable:="cbsa", filterValue:=14454)), _
    aggregations:=Array(sumAggregation(variableName:="population")), _
    groupby:=Array("cbsa", "year"), order:=Array("year"), _
    join:=apiQueryParameters( _
        table:="geocookbook_metro_na_shapes_full", _
        dataFields:=Array("cbsa", "area", "name"), _
        dataFilters:=Array(equalToFilter(filterVariable:="cbsa", filterValue:=14454)), _
        aggregations:=Array(), _
        groupby:=Array("cbsa", "name"), _
        joinOn:=joinOnStructure(left:=Array("cbsa"), right:=Array("cbsa")), _
        queryType:="AREA"), _
    queryType:="COUNT")
```

In many cases, we need to derive data from two or more variables. For example, when calculating 
population density, we need to take the population and divide by the area. In this case, those two 
metrics come from different sources in the StratoDem Analytics database, and we need to `JOIN` two queries 
using the `join` argument. 

A `join` takes another `APIQueryParams` object to join (effectively joining the results of two SELECT statements),
with that new `APIQueryParams` object requiring an `on` argument, to tell the API service which column(s) to join on.

For example, `on={"left": [cbsa], "right": [cbsa]}` tells the API to join the two subqueries on the `cbsa` column.

## GeoJSON queries

> This query returns a GeoJSON FeatureCollection with median household income stored in properties for all census tracts within a 15-minute drive of the lat-lng

```python
from strato_query import SDAPIQuery, APIGeoJSONQueryParams, APIMedianQueryParams
from strato_query.filters import EqualToFilter, DrivetimeFilter

geojson = SDAPIQuery.query_api_json(
    APIGeoJSONQueryParams(
        properties=[
            'geoid11',
            'name',
            'median_hhi'
        ],
        data_fields=['geoid11', 'geometry', 'name'],
        table='geocookbook_tract_na_shapes_full',
        groupby=(),
        data_filters=(),
        aggregations=(),
        join=APIMedianQueryParams(
            on={'left': ['geoid11'], 'right': ['geoid']},
            table='incomeforecast_tract_annual_income_group',
            median_variable_name='income_g',
            data_fields=[{'geoid11': 'geoid'}, {'median_value': 'median_hhi'}],
            data_filters=[
                EqualToFilter('year', 2019),
                DrivetimeFilter(latitude=42.1, longitude=-120.1, minutes=15, detailed_type='drivetime_unweighted'),
            ],
            groupby=['geoid11'],
            aggregations=(),
        )
    ))
```

```r
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": {\"query_type\": \"GEOJSON\", \"data_fields\": [\"geoid11\", \"geometry\", \"name\"], \"table\": \"geocookbook_tract_na_shapes_full\", \"groupby\": [], \"data_filters\": [], \"aggregations\": [], \"join\": {\"query_type\": \"MEDIAN\", \"data_fields\": [{\"geoid11\": \"geoid\"}, {\"median_value\": \"median_hhi\"}], \"table\": \"incomeforecast_tract_annual_income_group\", \"groupby\": [\"geoid11\"], \"data_filters\": [{\"filter_type\": \"eq\", \"filter_value\": 2019, \"filter_variable\": \"year\"}, {\"filter_type\": \"drivetime_unweighted\", \"filter_value\": {\"latitude\": 42.1, \"longitude\": -120.1, \"minutes\": 15, \"traffic\": \"disabled\", \"start_time\": null}, \"filter_variable\": \"\"}], \"aggregations\": [], \"on\": {\"left\": [\"geoid11\"], \"right\": [\"geoid\"]}, \"median_variable_name\": \"income_g\"}, \"properties\": [\"geoid11\", \"name\", \"median_hhi\"]}}"
```

```vb
```

To return a GeoJSON `FeatureCollection`, use the `APIGeoJSONQueryParams`. This query structure adds the 
`properties` argument, which specifies which fields will show up in each `Feature`'s `properties` field in the GeoJSON response.

The example to the right returns the GeoJSON `FeatureCollection` for the one census tract within a 15-minute drive of 42.1,-120.1 (lat, lng).

`{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": ["DUMMY DATA HERE"]}, "properties": {"geoid11": 41037960100, "name": "Census Tract: 41037960100", "median_hhi": 42182}}]}`

## Geocoder queries

> This query returns the census tract containing the latitude-longitude coordinates

```python
from strato_query import SDAPIQuery, APIGeocoderQueryParams

df_tract = SDAPIQuery.query_api_df(
    APIGeocoderQueryParams(
        data_fields=('geoid11', 'name'),
        # The geometry table for census tracts
        table='geocookbook_tract_na_shapes_full',
        latitude=42.3498224,
        longitude=-71.0521391,
        groupby=(),
        data_filters=(),
        aggregations=(),
    )
)

df_metro = SDAPIQuery.query_api_df(
    APIGeocoderQueryParams(
        data_fields=('cbsa', 'name'),
        # The geometry table for metros
        table='geocookbook_metro_na_shapes_full',
        latitude=42.3498224,
        longitude=-71.0521391,
        groupby=(),
        data_filters=(),
        aggregations=(),
    )
)
```

```r
# Not implemented yet
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": {\"query_type\": \"GEOCODER\", \"data_fields\": [\"cbsa\", \"name\"], \"table\": \"geocookbook_metro_na_shapes_full\", \"groupby\": [], \"data_filters\": [], \"aggregations\": [], \"latitude\": 42.3498224, \"longitude\": -71.0521391}}"
```

```vb
' Not implemented yet
```

To identify which geography contains a given location, the `APIGeocoderParams` take a 
geographic shapes table, a latitude, and a longitude, and construct a query to return the 
geographic ID.

The first example to the right returns the census tract ID (`GEOID11`) for the latitude-longitude pair.

|GEOID11|NAME|
|-------|----|
|25025061200|Census Tract: 25025061200|

The second example returns the metro ID for the latitude-longitude pair:

|CBSA|NAME|
|----|----|
|14454|Boston, MA|

## Custom polygon queries

> This query returns the population contained within the custom polygon by year

```python
from strato_query import SDAPIQuery, APIQueryParams
from strato_query.filters import IntersectsFilter, BetweenFilter
from strato_query.aggregations import SumAggregation

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
```

```r
# Not implemented yet
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": {\"query_type\": \"COUNT\", \"data_fields\": [\"year\", \"population\"], \"table\": \"populationforecast_tract_annual_population\", \"groupby\": [\"year\"], \"data_filters\": [{\"filter_type\": \"intersects_weighted\", \"filter_value\": {\"type\": \"Polygon\", \"coordinates\": [[[-71.17801666259767, 42.43321295705304], [-71.0145950317383, 42.43321295705304], [-71.0145950317383, 42.3145122534915], [-71.17801666259767, 42.3145122534915], [-71.17801666259767, 42.43321295705304]]]}, \"filter_variable\": \"geoid11\"}, {\"filter_type\": \"between\", \"filter_value\": [2010, 2019], \"filter_variable\": \"year\"}], \"aggregations\": [{\"aggregation_func\": \"sum\", \"variable_name\": \"population\"}], \"order\": [\"year\"]}}"
```

```vb
' Not implemented yet
```

To use a provided GeoJSON `Polygon` as a filter, use the `IntersectsFilter`.

The example to the right returns the population by year for the area covered by the provided `Polygon`

`{"type": "Polygon", "coordinates": [[[-71.1326, 42.2981],[-70.9943, 42.2981], [-70.9943, 42.3859],[-71.1326, 42.3859], [-71.1326, 42.2981]]]}`

|YEAR|SUM_POPULATION|
|-------|----|
|2010|852183|
|2011|862990|
|....|......|

## Advanced queries

> This query returns GDP per capita estimates for counties

```python
from strato_query import SDAPIQuery, APICalculationQueryParams, APIQueryParams
from strato_query.filters import EqualToFilter

df = SDAPIQuery.query_api_df(
    APICalculationQueryParams(
        data_fields=(
            'year',
            'geoid5',
            'real_gp',
            # Take the real_gp column and divide by population to get gdp_per_capita
            {'calculate:gdp_per_capita': 'real_gp / population'}),
        table='',
        aggregations=(),
        groupby=(),
        data_filters=(),
        inner_query=APIQueryParams(
            data_fields=('year', 'geoid5', 'real_gp'),
            data_filters=(EqualToFilter('month', 6),),
            table='grossproduct_county_monthly_forecasts',
            aggregations=(),
            groupby=(),
            join=APIQueryParams(
                data_fields=({'year': 'year_pop'}, {'geoid5': 'geoid5_pop'}, 'population'),
                data_filters=(),
                table='populationforecast_county_annual_population',
                aggregations=(),
                groupby=(),
                on={'left': ['year', 'geoid5'], 'right': ['year_pop', 'geoid5_pop']}
            ))))
```

```r
# Not yet in R
```

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": {\"query_type\": \"CALCULATION\", \"data_fields\": [\"year\", \"geoid5\", \"real_gp\", {\"calculate:gdp_per_capita\": \"real_gp / population\"}], \"table\": \"\", \"groupby\": [], \"data_filters\": [], \"aggregations\": [], \"inner_query\": {\"query_type\": \"COUNT\", \"data_fields\": [\"year\", \"geoid5\", \"real_gp\"], \"table\": \"grossproduct_county_monthly_forecasts\", \"groupby\": [], \"data_filters\": [{\"filter_type\": \"eq\", \"filter_value\": 6, \"filter_variable\": \"month\"}], \"aggregations\": [], \"join\": {\"query_type\": \"COUNT\", \"data_fields\": [{\"year\": \"year_pop\"}, {\"geoid5\": \"geoid5_pop\"}, \"population\"], \"table\": \"populationforecast_county_annual_population\", \"groupby\": [], \"data_filters\": [], \"aggregations\": [], \"on\": {\"left\": [\"year\", \"geoid5\"], \"right\": [\"year_pop\", \"geoid5_pop\"]}}}}}"
```

```vb
' Not yet in VB
```

To compute derivative values, a `APICalculationQueryParams` may be used.

These queries allow for computing values based on multiple columns. For example, GDP per capita 
estimates may be created as the local market output estimate divided by the population estimate.
