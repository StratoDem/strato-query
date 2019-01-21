library(jsonlite)

#' This function structures an API query to submit to the StratoDem Analytics API
#' @param table Table name
#' @param query_type Type of query - defaults to 'COUNT'
#' @param data_fields List of fields to return
#' @param data_filters List of filters for the query
#' @param aggregations List of aggregations for the query
#' @param groupby List of variables for GROUP BY
#' @keywords query
#' @export
#' @return query parameters
#' @examples
#' api_query_params('my-table', data_fields=list(), data_filters=list())
api_query_params = function(table, query_type = 'COUNT', data_fields, data_filters, aggregations = list(), groupby = list(), median_variable_name = NULL) {
  query = list(
    table = unbox(table),
    query_type = unbox(query_type),
    data_fields = data_fields,
    data_filters = data_filters,
    aggregations = aggregations,
    groupby = groupby,
    median_variable_name = unbox(median_variable_name)
  )

  return(query)
}

#' This function structures an API query to submit to the StratoDem Analytics API
#' @param table Table name
#' @param median_variable_name Name of median variable to use
#' @param data_fields List of fields to return
#' @param data_filters List of filters for the query
#' @param aggregations List of aggregations for the query
#' @param groupby List of variables for GROUP BY
#' @keywords query
#' @export
#' @return query parameters
#' @examples
#' median_query_params('my-table', data_fields=list(), data_filters=list())
median_query_params = function(table, data_fields, data_filters, median_variable_name, aggregations = list(), groupby = list()) {
  return(api_query_params(
    table = table,
    query_type = 'MEDIAN',
    data_fields = data_fields,
    data_filters = data_filters,
    aggregations = aggregations,
    groupby = groupby,
    median_variable_name = median_variable_name
  ))
}
