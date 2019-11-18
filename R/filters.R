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
    filter_variable = jsonlite::unbox(filter_variable),
    filter_type = jsonlite::unbox(filter_type),
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

#' Helper function to create a "not in" filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' nin_filter(filter_variable = 'year', filter_value = c(2018, 2023))
nin_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'nin', filter_value = filter_value))
}

#' Helper function to create an "equal to" filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' eq_filter(filter_variable = 'year', filter_value = 2018)
eq_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'eq', filter_value = jsonlite::unbox(filter_value)))
}

#' Helper function to create a "not equal to" filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' ne_filter(filter_variable = 'year', filter_value = 2018)
ne_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'ne', filter_value = jsonlite::unbox(filter_value)))
}

#' Helper function to create a "greater than" filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' gt_filter(filter_variable = 'year', filter_value = 2018)
gt_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'gt', filter_value = jsonlite::unbox(filter_value)))
}

#' Helper function to create a "greater than or equal to" filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' ge_filter(filter_variable = 'year', filter_value = 2018)
ge_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'ge', filter_value = jsonlite::unbox(filter_value)))
}

#' Helper function to create a "less than" filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' lt_filter(filter_variable = 'year', filter_value = 2018)
lt_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'lt', filter_value = jsonlite::unbox(filter_value)))
}

#' Helper function to create a "less than or equal to" filter
#' @param filter_variable Variable filtered on
#' @param filter_value Value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' le_filter(filter_variable = 'year', filter_value = 2018)
le_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = filter_variable, filter_type = 'le', filter_value = jsonlite::unbox(filter_value)))
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

#' Helper function to create an intersects filter
#' @param filter_variable Unused
#' @param filter_value Geojson value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' intersects_filter(filter_variable = '', filter_value)
intersects_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = '', filter_type = 'intersects', filter_value = filter_value))
}

#' Helper function to create an intersects_weighted filter
#' @param filter_variable Unused
#' @param filter_value Geojson value used for filter
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' intersects_weighted_filter(filter_variable = '', filter_value)
intersects_weighted_filter = function(filter_variable, filter_value) {
  return(api_filter(filter_variable = '', filter_type = 'intersects_weighted', filter_value = filter_value))
}

#' Helper function to create a drivetime filter
#' @param latitude Latitude of target
#' @param longitude Longitude of target
#' @param filter_type Full name of type of filter
#' @param minutes Minutes drivetime
#' @param traffic Traffic enabled or disabled
#' @param start_time What day and time to consider for traffic conditions, NULL for present conditions
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' drivetime_filter(latitude = 42.7, longitude = -120.38, filter_type = 'drivetime', minutes = 30, traffic = 'enabled', start_time = NULL)
drivetime_filter = function(latitude, longitude, filter_type, minutes, traffic, start_time) {
  return(
    api_filter(
      filter_variable = '',
      filter_type = jsonlite::unbox(filter_type),
      filter_value = list(
        latitude = jsonlite::unbox(latitude),
        longitude = jsonlite::unbox(longitude),
        minutes = jsonlite::unbox(minutes),
        traffic=jsonlite::unbox(traffic),
        start_time=jsonlite::unbox(start_time))))
}

#' Helper function to create a mile radius filter
#' @param latitude Latitude of target
#' @param longitude Longitude of target
#' @param filter_type Full name of type of filter
#' @param miles Size of radius in miles
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' mile_radius_filter(latitude = 42.7, longitude = -120.38, filter_type = 'mile_radius', miles = 5)
mile_radius_filter = function(latitude, longitude, filter_type, miles) {
  return(
    api_filter(
      filter_variable = '',
      filter_type = jsonlite::unbox(filter_type),
      filter_value = list(
        latitude = jsonlite::unbox(latitude),
        longitude = jsonlite::unbox(longitude),
        miles = jsonlite::unbox(miles))))
}

#' Helper function to create a walktime filter
#' @param latitude Latitude of target
#' @param longitude Longitude of target
#' @param filter_type Full name of type of filter
#' @param minutes Minutes walktime
#' @keywords query
#' @export
#' @return filter structure
#' @examples
#' walktime_filter(latitude = 42.7, longitude = -120.38, filter_type = 'walktime', minutes = 30)
walktime_filter = function(latitude, longitude, filter_type, minutes) {
  return(
    api_filter(
      filter_variable = '',
      filter_type = jsonlite::unbox(filter_type),
      filter_value = list(
        latitude = jsonlite::unbox(latitude),
        longitude = jsonlite::unbox(longitude),
        minutes = jsonlite::unbox(minutes))))
}
