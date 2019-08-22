# Authentication

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

```shell
$ curl -X POST "https://api.stratodem.com/api" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{ \"token\": \"my-api-token\", \"query\": { \"query_type\": \"MEDIAN\", \"data_fields\": [ \"year\", { \"median_value\": \"median_income\" } ], \"table\": \"incomeforecast_us_annual_income_group_age\", \"groupby\": [ \"year\" ], \"data_filters\": [ { \"filter_type\": \"ge\", \"filter_value\": 17, \"filter_variable\": \"age_g\" }, { \"filter_type\": \"between\", \"filter_value\": [ 2010, 2013 ], \"filter_variable\": \"year\" } ], \"aggregations\": [], \"order\": [ \"year\" ], \"median_variable_name\": \"income_g\"}}"
```

```vb
' Pass a valid API token to the query
' If you are using the provided template, you can place the API token in the Configuration!B5 cell
```

StratoDem Analytics uses API keys to allow access to the API. You can register a new StratoDem Analytics API key from your [account page](https://clients.stratodem.com/account).

[How do I create a new API token or find an existing token? &rarr;](https://academy.stratodem.com/article/82-creating-and-managing-api-tokens)

<aside class="notice">
You must replace <code>my-api-token</code> with your personal API key.
</aside>
