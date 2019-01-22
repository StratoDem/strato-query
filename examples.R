library(stRatoQuery)
apiToken = 'my-api-token'

# Median household income for all counties in California by year
df_ca_hhi = submit_api_query(
  query = median_query_params(
    table = 'incomeforecast_county_annual_income_group',
    data_fields = api_fields(fields_list = list(
      'year',
      'geoid5',
      # Rename the default 'median_value' column name to 'median_hhi'
      list(median_value = 'median_hhi'))),
    data_filters = list(
      # WHERE GEOID2 = 6 --> California has GEOID2 equal to 6
      eq_filter(filter_variable = 'geoid2', filter_value = 6)
    ),
    groupby = c('year', 'geoid2'),
    median_variable_name = 'income_g',
    aggregations = list()),
  apiToken = apiToken)
head(df_ca_hhi)

# 80+ households with at least $250,000 in household net worth by census tract in Suffolk County, MA
df_ma_80plus_nw = submit_api_query(
  query = api_query_params(
    table = 'networth_tract_annual_net_worth_age',
    data_fields = api_fields(fields_list = list(
      'geoid11',
      # Rename the 'households' field to 'hh_80plus_250k_nw'
      list(households = 'hh_80plus_250k_nw')
    )),
    data_filters = list(
      # WHERE GEOID5 = 25025 --> Suffolk County, MA has GEOID5 equal to 25025
      eq_filter(filter_variable = 'geoid5', filter_value = 25025),
      in_filter(filter_variable = 'year', filter_value = c(2013, 2018, 2023)),
      # Filter to 80+ households
      ge_filter(filter_variable = 'age_g_bottom_coded', filter_value = 17),
      # Filter to households with at least $250,000 in net worth
      ge_filter(filter_variable = 'net_worth_g', filter_value = 7)
    ),
    # Sum the households by year and geoid11
    aggregations = list(sum_aggregation(variable_name = 'households')),
    groupby = c('year', 'geoid11')
  ),
  apiToken = apiToken)
head(df_ma_80plus_nw)


# Population 25 to 39 by state with state names added to the results for data starting in 2010
df_senior_population = submit_api_query(
  api_query_params(
    table = 'populationforecast_state_annual_population_age',
    data_fields = api_fields(fields_list = list('year', 'geoid2', list(population = 'population_25_to_39'))),
    data_filters = list(
      # Filter to population between 25 and 39 (inclusive)
      between_filter(filter_variable = 'age_g', filter_value = c(6, 8)),
      # Get data starting in 2010
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
head(df_senior_population)
