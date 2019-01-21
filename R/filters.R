library(jsonlite)

#' Helper function to create an API filter
#' @param filter_variable Variable filtered on
#' @param filter_type Filter type ('eq' or 'in', e.g.)
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' api_filter(filter_type = 'eq', filter_variable = 'year', filter_value = 2018)
api_filter = function(filter_variable, filter_type, filter_value) {
  return(list(
    filter_variable = unbox(filter_variable),
    filter_type = unbox(filter_type),
    filter_value = filter_value
  ))
}

#' Helper function to create an IN filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' in_filter(filter_variable = 'year', filter_value = c(2018, 2023))
in_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'in', filter_value = filter_value))
}

#' Helper function to create an EQ filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' eq_filter(filter_variable = 'year', filter_value = 2018)
eq_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'eq', filter_value = unbox(filter_value)))
}

#' Helper function to create a between filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' between_filter(filter_variable = 'year', filter_value = c(2013, 2018))
between_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'between', filter_value = filter_value))
}
