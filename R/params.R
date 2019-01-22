library(jsonlite)

#' This function structures an API query to submit to the StratoDem Analytics API
#' @param table Table name
#' @param query_type Type of query - defaults to 'COUNT'
#' @param data_fields List of fields to return
#' @param data_filters List of filters for the query
#' @param aggregations List of aggregations for the query
#' @param groupby List of variables for GROUP BY
#' @param order List of variables to ORDER
#' @keywords query
#' @export
#' @return query parameters
#' @examples
#' # Returns 80+ population for Massachusetts and California from 2010 onward, sorted by year and state ID
#' api_query_params(
#'   table = 'populationforecast_state_annual_population_age',
#'   data_fields = api_fields(fields_list = list('year', 'geoid2', list(population = 'population_80_plus'))),
#'   data_filters = list(
#'     ge_filter(filter_variable = 'age_g', filter_value = 17),
#'     in_filter(filter_variable = 'geoid2', filter_value = c(6, 25)),
#'     ge_filter(filter_variable = 'year', filter_value = 2010)),
#'   aggregations = list(sum_aggregation(variable_name = 'population')),
#'   groupby = c('year', 'geoid2'),
#'   order = c('year', 'geoid2'))
api_query_params = function(table, query_type = 'COUNT', data_fields, data_filters, aggregations = list(), groupby = list(),
                            order = list(), median_variable_name = NA, mean_variable_name = NA, join = NA, on = NA) {
  if (is.na(on) && is.na(join)) {
    query = list(
      table = jsonlite::unbox(table),
      query_type = jsonlite::unbox(query_type),
      data_fields = data_fields,
      data_filters = data_filters,
      aggregations = aggregations,
      groupby = groupby,
      order = order,
      median_variable_name = jsonlite::unbox(median_variable_name),
      mean_variable_name = jsonlite::unbox(mean_variable_name),
      join = jsonlite::unbox(NA),
      on = jsonlite::unbox(NA)
    )
  } else if (is.na(on) && !is.na(join)) {
    query = list(
      table = jsonlite::unbox(table),
      query_type = jsonlite::unbox(query_type),
      data_fields = data_fields,
      data_filters = data_filters,
      aggregations = aggregations,
      groupby = groupby,
      order = order,
      median_variable_name = jsonlite::unbox(median_variable_name),
      mean_variable_name = jsonlite::unbox(mean_variable_name),
      join = join,
      on = jsonlite::unbox(NA)
    )
  } else if (!is.na(on) && is.na(join)) {
    query = list(
      table = jsonlite::unbox(table),
      query_type = jsonlite::unbox(query_type),
      data_fields = data_fields,
      data_filters = data_filters,
      aggregations = aggregations,
      groupby = groupby,
      order = order,
      median_variable_name = jsonlite::unbox(median_variable_name),
      mean_variable_name = jsonlite::unbox(mean_variable_name),
      join = jsonlite::unbox(NA),
      on = on
    )
  } else {
    query = list(
      table = jsonlite::unbox(table),
      query_type = jsonlite::unbox(query_type),
      data_fields = data_fields,
      data_filters = data_filters,
      aggregations = aggregations,
      groupby = groupby,
      order = order,
      median_variable_name = jsonlite::unbox(median_variable_name),
      mean_variable_name = jsonlite::unbox(mean_variable_name),
      join = join,
      on = on
    )
  }

  return(query)
}

#' This function structures an API query that gets the median value of the target "median_variable_name" to submit to the StratoDem Analytics API
#' @param table Table name
#' @param median_variable_name Name of median variable to use
#' @param data_fields List of fields to return
#' @param data_filters List of filters for the query
#' @param aggregations List of aggregations for the query
#' @param groupby List of variables for GROUP BY
#' @param order List of variables for ORDER
#' @keywords query
#' @export
#' @return query parameters
#' @examples
#' # Returns median household income by county in 2018
#' api_query_params(
#'   table = 'incomeforecast_county_annual_income_g',
#'   data_fields = api_fields(fields_list = list('geoid5', list(median_value = 'median_hhi'))),
#'   data_filters = list(eq_filter(filter_variable = 'year', filter_value = 2018)),
#'   aggregations = list(),
#'   median_variable_name = 'income_g',
#'   groupby = c('geoid5'),
#'   order = c('geoid5'))
median_query_params = function(table, data_fields, data_filters, median_variable_name, aggregations = list(),
                               groupby = list(), order = list(), join = NA, on = NA) {
  return(api_query_params(
    table = table,
    query_type = 'MEDIAN',
    data_fields = data_fields,
    data_filters = data_filters,
    aggregations = aggregations,
    groupby = groupby,
    order = order,
    median_variable_name = median_variable_name,
    join = join,
    on = on
  ))
}

#' This function structures an API query that gets the average value of the target "mean_variable_name" to submit to the StratoDem Analytics API
#' @param table Table name
#' @param mean_variable_name Name of mean variable to use
#' @param data_fields List of fields to return
#' @param data_filters List of filters for the query
#' @param aggregations List of aggregations for the query
#' @param groupby List of variables for GROUP BY
#' @keywords query
#' @export
#' @return query parameters
#' @examples
#' # Returns average household income by state in 2018
#' api_query_params(
#'   table = 'incomeforecast_state_annual_mean_household_income',
#'   data_fields = api_fields(fields_list = list('geoid2', list(mean_value = 'mean_hhi'))),
#'   data_filters = list(eq_filter(filter_variable = 'year', filter_value = 2018)),
#'   aggregations = list(),
#'   mean_variable_name = 'mean_household_income',
#'   groupby = c('geoid2'),
#'   order = c('geoid2'))
mean_query_params = function(table, data_fields, data_filters, mean_variable_name, aggregations = list(), groupby = list(),
                             order = list(), join = NA, on = NA) {
  return(api_query_params(
    table = table,
    query_type = 'MEAN',
    data_fields = data_fields,
    data_filters = data_filters,
    aggregations = aggregations,
    groupby = groupby,
    mean_variable_name = mean_variable_name,
    order = order,
    join = join,
    on = on
  ))
}
