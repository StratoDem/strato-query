library(httr)
library(jsonlite)

API_URL = 'https://api.stratodem.com/api'


#' This function submits an API query object as JSON to the StratoDem Analytics API
#' @param query Query object to submit to the StratoDem Analytics API
#' @param apiToken API token for authentication
#' @keywords query
#' @export
#' @return data.frame
#' @examples
#' submit_api_query(list(), 'my-api-token')
submit_api_query = function(query, apiToken) {
  json_request = list(token = jsonlite::unbox(apiToken), query = query)

  response = httr::POST(
    url = API_URL,
    body = jsonlite::toJSON(json_request),
    encode = 'json',
    accept_json())

  cont <- content(response)

  if (!cont$success) stop(cont$message)

  return(as.data.frame(do.call(rbind, cont$data)))
}
