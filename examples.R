library(httr)
library(jsonlite)
apiToken = 'my-api-token-here'

devtools::install_github("StratoDem/strato-query")
library(stRatoQuery)

r = submit_api_query(
  query = median_query_params(
    table = 'incomeforecast_state_annual_income_group',
    data_fields = api_fields(fields_list = list('year', 'geoid2', list(median_value = 'median_hhi'))),
    data_filters = list(
      in_filter(filter_variable = 'geoid2', filter_value = c(6))),
    groupby=c('year', 'geoid2'),
    median_variable_name='income_g',
    aggregations=list()
  ),
  apiToken = apiToken)
plot(r$year, r$median_hhi, type = 'l', main = 'California median household income', xlab = 'Year', ylab = '$')
