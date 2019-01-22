library(jsonlite)

#' Helper function to create an API aggregation
#' @param aggregation_func Aggregation function
#' @param variable_name Name of variable to aggregate
#' @keywords query
#' @export
#' @return aggregation structure
#' @examples
#' api_aggregation(aggregation_func = 'sum', variable_name = 'population')
api_aggregation = function(aggregation_func, variable_name) {
  return(list(
    aggregation_func = jsonlite::unbox(aggregation_func),
    variable_name = jsonlite::unbox(variable_name)
  ))
}

#' Helper function to create an API sum aggregation
#' @param variable_name Name of variable to aggregate
#' @keywords query
#' @export
#' @return aggregation structure
#' @examples
#' sum_aggregation(variable_name = 'population')
sum_aggregation = function(variable_name) {
  return(api_aggregation(aggregation_func = 'sum', variable_name = variable_name))
}

#' Helper function to create an API mean aggregation
#' @param variable_name Name of variable to aggregate
#' @keywords query
#' @export
#' @return aggregation structure
#' @examples
#' mean_aggregation(variable_name = 'population')
mean_aggregation = function(variable_name) {
  return(api_aggregation(aggregation_func = 'mean', variable_name = variable_name))
}
