# Changelog for strato-query

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## [2.6.4] - 2019-02-20
### Changes
- Changes the VBA docs to give a more detailed account of how to use and update queries

## [2.6.3] - 2019-02-12
### Fixes
- Fixes `APIQueryParams.pretty_print_vba` for mile radius and drivetime filters

## [2.6.2] - 2019-02-01
### Fixes
- Fixes a bug caused by users running the code without a debug token. The debug token has been removed and the code will rely on the actual API token

## [2.6.1] - 2019-01-28
### Fixes
- Fixes reference to image names in docs

## [2.6.0] - 2019-01-28
### Adds
- Adds examples to the docs showing how to use Blaise ML to generate API queries for each supported language

## [2.5.6] - 2019-01-26
### Adds
- Adds `MileRadiusFilter` and `DrivetimeFilter` to `strato_query`
- Updates `submit_api_query` to return `data.frame` with correct `numeric` types in R

## [2.5.5] - 2019-01-25
### Fixes
- Adds spacing for comma-separated arguments

## [2.5.4] - 2019-01-25
### Fixes
- Bug fixes in `pretty_print_r` and `pretty_print_vba` for `query_type`

## [2.5.3] - 2019-01-25
### Fixes
- Fixes argument name in `pretty_print` method

## [2.5.2] - 2019-01-25
### Adds
- Adds a pretty print method that can be called on the `APIQueryParams` class, and any class inheriting from the same.
It will return a string that mirrors R code, and can be copied and pasted directly into an R script.

## [2.5.1] - 2019-01-25
### Adds
- Adds a pretty print method that can be called on the `APIQueryParams` class, and any class inheriting from the same.
It will return a string that mirrors Excel VBA code, and can be copied and pasted directly into a VBA script.

## [2.5.0] - 2019-01-25
### Adds
- Adds a pretty print method that can be called on the `APIQueryParams` class, and any class inheriting from the same.
It will return a string that mirrors the Python code, and can be copied and pasted directly into a Python script.
- Adds default values for the `query_type`, allowing this value to be omitted when creating instances of the `APIQueryParams` classes

## [2.4.0] - 2019-01-09
### Adds
- Adds example queries to demonstrate different ways of using `strato-query`

## [2.3.1] - 2019-01-06
### Changes
- `BaseAPIQuery.submit_query` now includes optional `headers` argument to send with request

## [2.3.0] - 2019-01-03
### Adds
- Adds new filters to `__all__` declaration
- Adds new classes, `APIMeanQueryParams` and `APIMedianQueryParams`, which require the values necessary for the related queries
- Adds new tests for the new query types

## [2.2.0] - 2019-01-02
### Adds
- Adds new filters for "not in" and "not equal"

## [2.1.2] - 2018-12-27
### Adds
- Adds optional `median_variable_name` parameter to `APIQueryParams` to allow for median queries

## [2.1.1] - 2018-12-27
### Adds
- Adds optional `order` parameter to `APIQueryParams` to allow for sorting results

## [2.1.0] - 2018-12-27
### Changes
- Changes the `InFilter` so it will raise an error if it receives an empty list or `None` as the `val`.

## [2.0.0] - 2018-12-26
### Changes
- **Breaking change**. Combines the query param classes into one while allowing for unlimited nesting of joins.

Example use:

```python
from strato_query.base_API_query import *
from strato_query.standard_filters import *

class ExampleAPIJoinQuery(BaseAPIQuery):
    @classmethod
    def get_df_from_API_call(cls, **kwargs):
        df = cls.query_api_df(
            query_params=APIQueryParams(
                table='table_1',
                data_fields=('a', 'b', 'c'),
                data_filters=(),
                query_type='COUNT',
                aggregations=(),
                groupby=(),
                join=APIQueryParams(
                    table='table_2',
                    data_fields=('c', 'd'),
                    data_filters=(),
                    query_type='COUNT',
                    aggregations=(),
                    groupby=(),
                    on=dict(left=('c',), right=('c',)),
                    join=APIQueryParams(
                        table='table_3',
                        data_fields=('d',),
                        data_filters=(),
                        query_type='COUNT',
                        aggregations=(),
                        groupby=(),
                        on=dict(left=('d',), right=('d',)),
                    )
                )
            )
        )

        return df
```

## [1.0.0] - 2018-12-26
### v1 release
- Version 1.0.0 release
