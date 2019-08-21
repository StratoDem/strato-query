---
title: StratoDem Analytics API

language_tabs: # must be one of https://git.io/vQNgJ
  - python
  - r
  - javascript
  - shell
  - visualbasic

toc_footers:
  - <a href='https://stratodem.com'>StratoDem Analytics</a>
  - <a href='https://github.com/StratoDem/strato-query'>strato-query repository</a>
  - <a href='https://github.com/tripit/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true
---

# Introduction

Welcome to the StratoDem Analytics API. You can use the API to query economic and geo-demographic data from the StratoDem Analytics database.

We have language bindings in Python, R and VBA (for Excel). You can view code examples in the dark area to the right, and you can switch the programming language of the examples with the tabs in the top right.

# Installation

Install from PyPI or GitHub

```python
$ pip install strato-query
```

```r
library(devtools)
devtools::install_github('StratoDem/strato-query')
```

# Authentication

StratoDem Analytics uses API keys to allow access to the API. You can register a new StratoDem Analytics API key from your [account page](https://clients.stratodem.com/account).

[How do I create a new API token or find an existing token? &rarr;](https://academy.stratodem.com/article/82-creating-and-managing-api-tokens)

> To authorize, use this code:

```python
from strato_query import authenticate_to_api

# Option 1: Pass in the API token as a string
authenticate_to_api('my-api-token')

# Option 2: Pass in the API token via an environment variable at STRATODEM_API_TOKEN
# This would be, e.g., $ STRATODEM_API_TOKEN=my-api-token python my_api_script.py
authenticate_to_api()

# API calls from this point on will now query the API with API_TOKEN
```

```r
library(stRatoquery)

# This requires an apiToken argument for each submitted API query
df = submit_api_query(query = myQueryParams, apiToken = 'my-api-token')
```

<aside class="notice">
You must replace <code>my-api-token</code> with your personal API key.
</aside>

# Submitting a query

```python
from strato_query import SDAPIQuery, APIMedianQueryParams, GreaterThanOrEqualToFilter, BetweenFilter

# Finds median household income in the US for those 80+ from 2010 to 2013
df = SDAPIQuery.query_api_df(
    query_params=APIMedianQueryParams(
        query_type='MEDIAN',
        table='incomeforecast_us_annual_income_group_age',
        data_fields=('year', {'median_value': 'median_income'}),
        median_variable_name='income_g',
        data_filters=(
            GreaterThanOrEqualToFilter(var='age_g', val=17).to_dict(),
            BetweenFilter(var='year', val=[2010, 2013]).to_dict(),
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

# Finds median household income in the US for those 80+ from 2010 to 2013
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

A basic query to the StratoDem Analytics API submits query parameters with authentication via the API token.

# Query parameters

# Filters
