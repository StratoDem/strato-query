library(httr)
library(jsonlite)
apiToken = 'my-api-token-here'

devtools::install_github("StratoDem/strato-query")
library(stRatoQuery)

library(stRatoquery)

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

r = submit_api_query(
  query = median_query_params(
    table = 'networth_tract_annual_net_worth',
    data_fields = api_fields(fields_list = list('year', list(median_value = 'median_nw'))),
    data_filters = list(drivetime_filter(latitude = 42.3498224, longitude = -71.0521391, minutes = 15)),
    groupby=c('year'),
    median_variable_name='net_worth_g',
    aggregations=list()
  ),
  apiToken = apiToken)
plot(r$year, r$median_nw, type = 'l', main = 'Median net worth within 15-minute drive of lat-lng pair', xlab = 'Year', ylab = '$')

submit_api_query(
  api_query_params(
    table = 'populationforecast_state_annual_population_age',
    data_fields = api_fields(fields_list = list('year', 'geoid2', list(population = 'population_80_plus'))),
    data_filters = list(
      ge_filter(filter_variable = 'age_g', filter_value = 17),
      in_filter(filter_variable = 'geoid2', filter_value = c(6, 25)),
      ge_filter(filter_variable = 'year', filter_value = 2010)),
    aggregations = list(sum_aggregation(variable_name = 'population')),
    groupby = c('year', 'geoid2'),
    order = c('year', 'geoid2'),
    join = api_query_params(
      table = "geocookbook_state_na_state_name",
      data_fields = api_fields(c("geoid2", "geoid2_name")),
      data_filters = list(),
      aggregations = list(),
      on = list(left = c('geoid2'), right = c('geoid2'))
    )),
  apiToken = apiToken)