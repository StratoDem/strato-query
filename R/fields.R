
#' This function structures api fields to query
#' @param fields_list A list of fields to query
#' @keywords query
#' @export
#' @return fields list
#' @examples
#' api_fields(list('year', 'geoid2', list(population = 'state_population')))
api_fields = function(fields_list = list()) {
  lapply(fields_list, function(el) {
    if (class(el) == 'character') return(unbox(el))
    else if (class(el) == 'list') {
      r = list()
      r [[names(el[1])]] = unbox(el[[1]])

      return(r)
    }
  })
}
