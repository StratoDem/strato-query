# Changelog for strato-query

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

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