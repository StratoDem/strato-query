# Aggregations

In many cases, we want to aggregate data returned by the API. For example, if we have the SQL query:
`SELECT year, geoid5, sum(households) FROM incomeforecast_county_annual_income_group_age WHERE income_g >= 5 AND age_g >= 17 GROUP BY year, geoid5 ORDER BY year, geoid5;`, 
we need to group by the `year` and `geoid5` (county) columns, and then get the sum of `households` for each combination.

Aggregrations tell the API which columns to aggregate, using which function.

## `SumAggregation`

> This tells the API to take the sum of population

```python
from strato_query.aggregations import SumAggregation

SumAggregation('population')
```

```r
library(stRatoquery)

sum_aggregation(variable_name = 'population')
```

```shell
{"aggregation_type": "sum", "variable_name": "population"}
```

```vb
sumAggregation(variableName:="population")
```

Sum aggregations tell the API to return the sum of the variable passed in, equivalent to `sum(variable_name)` in SQL
