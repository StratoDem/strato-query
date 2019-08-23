# Filters

## `EqualToFilter`

> Use this filter to restrict data to the year 2019

```python
from strato_query.filters import EqualToFilter

EqualToFilter(
    var='year',
    val=2019)
```

```r
library(stRatoquery)

eq_filter(filter_variable = 'year', filter_value = 2019)
```

```shell
{"filter_type": "eq", "filter_variable": "year", "filter_value": 2019}
```

```vb
equalToFilter(filterVariable:=”year”, filterValue:=2019)
```

The `EqualToFilter` constructs a filter equivalent to `var = val` comparisons.

## `BetweenFilter`

> Use this filter to restrict data where the age grouping is between 25 and 39 years old (inclusive)

```python
from strato_query.filters import BetweenFilter

BetweenFilter(var='age_g', val=[6, 8])
```

```r
library(stRatoquery)

between_filter(filter_variable = 'age_g', filter_value = c(6, 8))
```

```shell
{"filter_type": "between", "filter_variable": "age_g", "filter_value": [6, 8]}
```

```vb
betweenFilter(filterVariable:="age_g", filterValue:=Array(6, 8))
```

The `BetweenFilter` constructs a filter equivalent to `var >= val AND var <= val` comparisons.

## `InFilter`

> Use this filter to restrict data where the year is one of the allowed values

```python
from strato_query.filters import InFilter

InFilter(var='year', val=[2014, 2019, 2024])
```

```r
library(stRatoquery)

in_filter(filter_variable = 'year', filter_value = c(2014, 2019, 2024))
```

```shell
{"filter_type": "in", "filter_variable": "year", "filter_value": [2014, 2019, 2024]}
```

```vb
inFilter(filterValue:="year", filterValue:=Array(2014, 2019, 2024))
```

The `InFilter` constructs a filter equivalent to `var IN (val1, val2, val3)` comparisons.

## `GreaterThanFilter`

> Use this filter to restrict data where the educational attainment level is greater than high school

```python
from strato_query.filters import GreaterThanFilter

GreaterThanFilter(var='educational_attainment', val=2)
```

```r
library(stRatoquery)

gt_filter(filter_variable = 'educational_attainment', filter_value = 2)
```

```shell
{"filter_type": "gt", "filter_variable": "educational_attainment", "filter_value": 2}
```

```vb
greaterThanFilter(filterVariable:="educational_attainment", filterValue:=2)
```

The `GreaterThan` constructs a filter equivalent to `var > val` comparisons.

## `GreaterThanOrEqualToFilter`

> Use this filter to restrict data where the educational attainment level is greater than or equal to high school

```python
from strato_query.filters import GreaterThanOrEqualToFilter

GreaterThanOrEqualToFilter(var='educational_attainment', val=2)
```

```r
library(stRatoquery)

gte_filter(filter_variable = 'educational_attainment', filter_value = 2)
```

```shell
{"filter_type": "gte", "filter_variable": "educational_attainment", "filter_value": 2}
```

```vb
greaterThanOrEqualToFilter(filterVariable:="educational_attainment", filterValue:=2)
```

The `GreaterThanOrEqualTo` constructs a filter equivalent to `var >= val` comparisons.

## `LessThanFilter`

> Use this filter to restrict data where the educational attainment level is less than high school

```python
from strato_query.filters import LessThanFilter

LessThanFilter(var='educational_attainment', val=2)
```

```r
library(stRatoquery)

lt_filter(filter_variable = 'educational_attainment', filter_value = 2)
```

```shell
{"filter_type": "lt", "filter_variable": "educational_attainment", "filter_value": 2}
```

```vb
lessThanFilter(filterVariable:="educational_attainment", filterValue:=2)
```

The `LessThan` constructs a filter equivalent to `var > val` comparisons.

## `LessThanOrEqualToFilter`

> Use this filter to restrict data where the educational attainment level is less than or equal to high school

```python
from strato_query.filters import LessThanOrEqualToFilter

LessThanOrEqualToFilter(var='educational_attainment', val=2)
```

```r
library(stRatoquery)

lte_filter(filter_variable = 'educational_attainment', filter_value = 2)
```

```shell
{"filter_type": "lte", "filter_variable": "educational_attainment", "filter_value": 2}
```

```vb
lessThanOrEqualToFilter(filterVariable:="educational_attainment", filterValue:=2)
```

The `LessThanOrEqualTo` constructs a filter equivalent to `var >= val` comparisons.

## `NotEqualToFilter`

> Use this filter to restrict data to all years except 2019

```python
from strato_query.filters import NotEqualToFilter

NotEqualToFilter(
    var='year',
    val=2019)
```

```r
library(stRatoquery)

ne_filter(filter_variable = 'year', filter_value = 2019)
```

```shell
{"filter_type": "ne", "filter_variable": "year", "filter_value": 2019}
```

```vb
notEqualTo(filterVariable:=”year”, filterValue:=2019)
```

The `NotEqualToFilter` constructs a filter equivalent to `var <> val` comparisons.

## `NotInFilter`

> Use this filter to restrict data where the year is not any of the specified values

```python
from strato_query.filters import NotInFilter

NotInFilter(var='year', val=[2014, 2019, 2024])
```

```r
library(stRatoquery)

nin_filter(filter_variable = 'year', filter_value = c(2014, 2019, 2024))
```

```shell
{"filter_type": "nin", "filter_variable": "year", "filter_value": [2014, 2019, 2024]}
```

```vb
notInFilter(filterValue:="year", filterValue:=Array(2014, 2019, 2024))
```

The `NotInFilter` constructs a filter equivalent to `var NOT IN (val1, val2, val3)` comparisons.

## `MileRadiusFilter`

> Use this filter to restrict results to geographies within a mile radius

```python
from strato_query.filters import MileRadiusFilter

MileRadiusFilter(latitude=40.7589, longitude=-73.9937, miles=5)

# This gets all geographies intersecting with the mile radius 
# (any amount of intersection), and does not apply weights
MileRadiusFilter(latitude=40.7590, longitude=-73.9937, miles=5, detailed_type='mile_radius_unweighted')
```

```r
library(stRatoquery)

mile_radius_filter(latitude = 40.7589, longitude = -73.9937, miles = 5)
```

```shell
{"filter_type": "mile_radius", "filter_variable": "", "filter_value": {"latitude": 40.7590, "longitude": -73.9936, "miles": 5}}
{"filter_type": "mile_radius_simple", "filter_variable": "", "filter_value": {"latitude": 40.7590, "longitude": -73.9936, "miles": 5}}
{"filter_type": "mile_radius_unweighted", "filter_variable": "", "filter_value": {"latitude": 40.7590, "longitude": -73.9936, "miles": 5}}
```

```vb
mileRadiusFilter(latitude:=40.7589, longitude:=-73.9937, miles:=5)
```

The `MileRadiusFilter` constructs a filter to restrict results to geographies intersecting/contained by the mile radius buffer

### Advanced options

An advanced option for the `MileRadiusFilter` is the `detailed_type` argument, which allows one of three options:

- `mile_radius` (default): Apply weights to the results based on the population-weighted intersection of the mile radius buffer and geographies
- `mile_radius_simple`: Apply weights to the results based on the population-weighted intersection of the mile radius buffer and simplified geographies
- `mile_radius_unweighted`: Do not apply weights. Only return all geographies intersecting with the mile radius buffer

## `DrivetimeFilter`

> Use this filter to restrict results to geographies within an estimated drive time

```python
from strato_query.filters import DrivetimeFilter

DrivetimeFilter(latitude=40.7589, longitude=-73.9937, minutes=15)
# Compute 15-minute drive with traffic
DrivetimeFilter(latitude=40.7589, longitude=-73.9937, minutes=15, with_traffic=True, start_time='2019-05-25T18:00:00')
# This gets all geographies intersecting with the drive time buffer
# (any amount of intersection) and does not apply weights
DrivetimeFilter(latitude=40.7589, longitude=-73.9937, minutes=15, detailed_type='drivetime_unweighted')
```

```r
library(stRatoquery)

drivetime_filter(latitude = 40.7589, longitude = -73.9937, minutes = 15)
```

```shell
{"filter_type": "drivetime", "filter_variable": "", "filter_value": {"latitude": 40.7590, "longitude": -73.9936, "minutes": 15}}
{"filter_type": "drivetime_simple", "filter_variable": "", "filter_value": {"latitude": 40.7590, "longitude": -73.9936, "minutes": 15}}
{"filter_type": "drivetime_unweighted", "filter_variable": "", "filter_value": {"latitude": 40.7590, "longitude": -73.9936, "minutes": 15}}
{"filter_type": "drivetime", "filter_variable": "", "filter_value": {"latitude": 40.7590, "longitude": -73.9936, "minutes": 15, "with_traffic": true, "start_time": "2019-05-25T18:00:00"}}
```

```vb
drivetimeFilter(latitude:=40.7589, longitude:=-73.9937, minutes:=5)
```

The `DrivetimeFilter` constructs a filter to restrict results to geographies intersecting/contained by the drive time buffer

### Advanced options

An advanced option for the `DrivetimeFilter` is the `detailed_type` argument, which allows one of three options:

- `drivetime` (default): Apply weights to the results based on the population-weighted intersection of the drive time buffer and geographies
- `drivetime_simple`: Apply weights to the results based on the population-weighted intersection of the drive time buffer and simplified geographies
- `drivetime_unweighted`: Do not apply weights. Only return all geographies intersecting with the drive time buffer

To compute drive time estimates with traffic, two arguments are used: `with_traffic` and `start_time`:

- `with_traffic` (defaults to `False`) toggles on (`True`) or off (`False`) traffic calculations
- `start_time` (defaults to `None`) adjusts the departure time used to compute the traffic buffer

## `IntersectsFilter`

> Use this filter to restrict results to geographies intersecting a GeoJSON Polygon

```python
from strato_query.filters import IntersectsFilter

IntersectsFilter(
    var='geometry', 
    val={
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-71.13269805908203, 42.298135272741206],
            [-70.99433898925781, 42.298135272741206],
            [-70.99433898925781, 42.385937107381125],
            [-71.13269805908203, 42.385937107381125],
            [-71.13269805908203, 42.298135272741206]
          ]]
      }
    })
```

```r
# Not implemented yet!
```

```shell
{"filter_type": "intersects", "filter_variable": "geometry", "filter_value": {"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [[[-71.13269805908203, 42.298135272741206], [-70.99433898925781, 42.298135272741206], [-70.99433898925781, 42.385937107381125], [-71.13269805908203, 42.385937107381125], [-71.13269805908203, 42.298135272741206]]]}}
```

```vb
' Not implemented yet!
```

The `IntersectsFilter` constructs a filter to restrict results to geographies intersecting the GeoJSON polygon
