## `stRatoquery`
Tools to help query the StratoDem Analytics API for economic and geo-demographic data in R

[Back to main page](/strato-query)

## Table of contents
- [Installation and usage](#installation-and-usage)
- [Authentication](#authentication)
- [Sample queries](#sample-queries)
  - [Median household income for 80+ households across the US, by year](#api-example-median-hhi)
  - [Population density in the Boston MSA](#api-example-population-density)
  - [Population within five miles of latitude-longitude pair](#api-example-mile-radius-filter)

### [Installation and usage](#installation-and-usage)

To install the `stRatoquery` R package:
```R
library(devtools)
devtools::install_github('StratoDem/strato-query')
```

### [Authentication](#authentication)
`stRatoquery::submit_api_query` requires an `apiToken` argument.

[How do I create a new API token or find an existing token? &rarr;](https://academy.stratodem.com/article/82-creating-and-managing-api-tokens)

### [Sample queries](#sample-queries)

#### [Median household income for 80+ households across the US, by year](#api-example-median-hhi)
```R
library(stRatoquery)

# Finds median household income in the US for those 80+ from 2010 to 2013
df = submit_api_query(
  query = median_query_params(
    table = 'incomeforecast_us_annual_income_group_age',
    data_fields = api_fields(fields_list = list('year', 'geoid2', list(median_value = 'median_hhi'))),
    data_filters = list(
        ge_filter(filter_variable = 'age_g', filter_value = 17),
        between_filter(filter_variable = 'year', filter_value = c(2010, 2013))
    ),
    groupby=c('year'),
    median_variable_name='income_g',
    aggregations=list()
  ),
  apiToken = 'my-api-token-here')

print('Median US household income 80+:')
print(head(df))
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

#### [Population density in the Boston MSA](#api-example-population-density)
```R
library(stRatoquery)

df = submit_api_query(
  query = api_query_params(
    table = 'populationforecast_metro_annual_population',
    data_fields = api_fields(fields_list = list('year', 'cbsa', list(population = 'population'))),
    data_filters = list(
        lt_filter(filter_variable = 'year', filter_value = 2015),
        eq_filter(filter_variable = 'cbsa', filter_value = 14454)
    ),
    groupby=c('year'),
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
  apiToken = 'my-api-token-here')
```

Output:
```
Population density in the Boston MSA up to 2015:
   YEAR        NAME  POP_PER_SQ_MI
0  2000  Boston, MA    1139.046639
1  2001  Boston, MA    1149.129937
2  2002  Boston, MA    1153.094740
3  2003  Boston, MA    1152.352351
4  2004  Boston, MA    1149.932307
Results truncated
```

### [Population within five miles of latitude-longitude pair](#api-example-mile-radius-filter)
```R
library(stRatoquery)

df = submit_api_query(
  api_query_params(
    table = 'populationforecast_tract_annual_population',
    data_fields = api_fields(fields_list = list('YEAR', list(population = 'population_within_5_miles'))),
    data_filters = list(
      # Aggregate data within five miles of 40.7589542, -73.9937348
      mile_radius_filter(latitude = 40.7589542, longitude = -73.9937348, miles = 5),
      # Only get data for years between 2010 and 2020 (inclusive)
      between_filter(filter_variable = 'year', filter_value = c(2010, 2020))),
    aggregations = list(sum_aggregation(variable_name = 'population')),
    groupby = c('year')),
  apiToken=apiToken)

head(df)
```

Output:
```
  year population_within_5_miles
1 2010                   2333013
2 2011                   2368923
3 2012                   2399682
4 2013                   2419962
5 2014                   2437614
6 2015                   2456257
```
