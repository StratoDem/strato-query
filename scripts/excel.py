"""
StratoDem Analytics : excel
Principal Author(s) : Owen Dreikosen
Secondary Author(s) :
Description : VBA package generation for Excel User-Defined Functions

Notes :

Naming Conventions

query = 1 specific type of query for the API
i.e STRATODEM_HOUSEHOLDS_WITH_INCOME_BETWEEN_FOR_METRO

function = multiple different variations for different
input variables and filters of queries -> queryHouseholdsIncomeAge

many queries -> 1 function

October 10, 2019
"""

import abc
import itertools
import re
from types import MappingProxyType
from typing import Tuple

# Map the metric to the default filter with all possible values of the metric
# (MappingProxyType so this is immutable)
map_metric_to_default_filter_values = MappingProxyType({
    'AGE': '\t\tAGE_LOW:=1, _ \n\t\tAGE_HIGH:=18, _\n',
    'INCOME': '\t\tINCOME_LOW:=1, _ \n\t\tINCOME_HIGH:=18, _\n'
})

# Map filter type to the filter dim definition in VBA function stub
# (MappingProxyType so this is immutable)
map_filter_type_to_filter_dim = MappingProxyType({
    'BETWEEN': 'XXX_LOW as Integer, XXX_HIGH as Integer, '
})

# Templates for all supported filters for the parameters for functions
# (MappingProxyType so this is immutable)
map_filter_type_to_filter_template = MappingProxyType({
    'BETWEEN': '\t\tXXX_LOW:=XXX_LOW, _\n\t\tXXX_HIGH:=XXX_HIGH, _\n'
})

# Map geographic level to dim definition in VBA function stub
# (MappingProxyType so this is immutable)
outer_geo_function_dim = MappingProxyType({
    'METRO': 'METRO_CODE As Long',
    # 'STATE': 'GEOID2',
    'COUNTY': 'COUNTY_CODE As Long',
    # 'US':'US',
    # "MICRO":'micro',
    # 'ZIP':"zip",
    # 'TRACT': 'GEOID11',
    'MILE_RADIUS': "LATITUDE As Double, LONGITUDE As Double, MILES As Double"
    # 'DRIVE_TIME':'drive_time'
})

# Map geographic level to geographic filter used in function
# (MappingProxyType so this is immutable)
inner_geo_filters = MappingProxyType({
    'METRO': '''\t\tgeoname:=\"metro\", _
    \t\tgeoFilter:=equalToFilter(\"cbsa\",METRO_CODE), _\n''',
    # 'STATE':'LOL',
    'COUNTY': '''\t\tgeoname:=\"county\", _
    \t\tgeoFilter:=equalToFilter(\"geoid5\",COUNTY_CODE), _\n''',
    # "US":"Still gotta do",
    # "MICRO":"WILL FINISH",
    # "ZIP":"I PROMISE",
    # "TRACT":"working on replicating the excel example first",
    "MILE_RADIUS": '''\t\tgeoname:=\"tract\", _
    \t\tgeoFilter:=mileRadiusFilter(LATITUDE:=LATITUDE,LONGITUDE:=LONGITUDE, MILES:=MILES), _\n'''
    # "DRIVE_TIME": "Okay last one"
})

# Template for end of VBA function
helper_function_template = '''
    numCols = dataResults("data")(1).Count
    columnNames = Array("households", "year")
    numObservations = dataResults("data").Count

    ReDim dataArray(numObservations - 1, numCols - 1)

    idxRow = 0
    For Each Value In dataResults("data")
        For idxCol = 0 To numCols - 1
            dataArray(idxRow, idxCol) = Value(columnNames(idxCol))
        Next idxCol
        idxRow = idxRow + 1
    Next Value

    XXX = dataArray
End Function\n\n'''


class StratoFunction(abc.ABC):
    user_variables = None
    function_title = None

    # Creates all possible combinations of queries with given input variables
    def __init__(self):
        self.queries = []
        self.vba_function_definition_str = None

        filters_and_data = []
        combos = []

        # TODO what is all this doing?? :D
        for _filter in map_filter_type_to_filter_dim.keys():
            for variable in self.user_variables:
                filters_and_data.append(f"WITH_{variable}_{_filter}_")
        for i in range(1, len(self.user_variables) + 1):
            combos.append(list(itertools.combinations(filters_and_data, i)))
        for combo in combos:
            for variable in combo:
                query = ''.join(variable)
                for geo in outer_geo_function_dim.keys():
                    self.queries.append(f"STRATODEM_{self.function_title}_{query}FOR_{geo}")
        for geo in outer_geo_function_dim.keys():
            self.queries.append(f"STRATODEM_{self.function_title}_FOR_{geo}")

    def params(self, vba_function_definition_str):
        for variable in self.user_variables:
            if variable not in vba_function_definition_str:
                vba_function_definition_str += map_metric_to_default_filter_values[variable]
        self.vba_function_definition_str = vba_function_definition_str

    @property
    @abc.abstractmethod
    def function_string(self):
        pass


class HouseholdsByIncomeStratoFunction(StratoFunction):
    user_variables = ['AGE', 'INCOME']
    function_title = 'HOUSEHOLDS'
    function_name = 'queryHouseholdsIncomeAge'

    @property
    def function_string(self) -> str:
        function_string = '''Public Function queryHouseholdsIncomeAge(YEAR_LOW As Integer, YEAR_HIGH As Integer, INCOME_LOW As Integer, INCOME_HIGH As Integer, AGE_LOW As Integer, AGE_HIGH As Integer, geoname As String, geoFilter As Dictionary, API_TOKEN As String) As Variant
    Dim dataResults As Object

    Set dataResults = submitAPIQuery( _
                      query:=apiQueryParameters( _
                              table:="incomeforecast_" & geoname & "_annual_income_group_age", _
                      dataFields:=Array(renameVariable(original:="households", renamed:="households"), "year"), _
                      dataFilters:=Array( _
                                    geoFilter, _
                      betweenFilter("year", Array(YEAR_LOW, YEAR_HIGH)), _
                      betweenFilter("income_g", Array(INCOME_LOW, INCOME_HIGH)), _
                      betweenFilter("age_g", Array(AGE_LOW, AGE_HIGH))), _
        aggregations:=Array(sumAggregation("households")), _
        groupby:=Array("year"), _
        order:=Array("year")), _
        API_TOKEN:=API_TOKEN)
''' + helper_function_template
        function_string = function_string.replace("XXX", self.function_name)

        return function_string


class MedianHouseholdIncomeStratoFunction(StratoFunction):
    user_variables = ['AGE']
    function_title = 'MEDIAN_HOUSEHOLD_INCOME'
    function_name = 'queryMedianIncomeAge'

    @property
    def function_string(self) -> str:
        function_string = '''Public Function queryMedianIncomeAge(YEAR_LOW As Integer, YEAR_HIGH As Integer, AGE_LOW As Integer, AGE_HIGH As Integer, geoname As String, geoFilter As Dictionary, API_TOKEN As String) As Variant
    Dim dataResults As Object

    Set dataResults = submitAPIQuery( _
                      query:=medianQueryParameters( _
                              table:="incomeforecast_" & geoname & "_annual_income_group_age", _
                      dataFields:=Array(renameVariable(original:="median_value", renamed:="median_hhi"), "year"), _
                      medianVariableName:="income_g", _
                      dataFilters:=Array( _
                                    geoFilter, _
                      betweenFilter("year", Array(YEAR_LOW, YEAR_HIGH)), _
                      betweenFilter("age_g", Array(AGE_LOW, AGE_HIGH))), _
        aggregations:=Array(sumAggregation("households")), _
        groupby:=Array("year"), _
        order:=Array("year")), _
        API_TOKEN:=API_TOKEN)
    ''' + helper_function_template
        function_string = function_string.replace("XXX", self.function_name)

        return function_string


# Map the function topic (e.g., 'HOUSEHOLDS') to the StratoFunction instance
map_function_topic_to_stratofunction = MappingProxyType({
    'HOUSEHOLDS': HouseholdsByIncomeStratoFunction(),
    'MEDIAN_HOUSEHOLD_INCOME': MedianHouseholdIncomeStratoFunction()
})


def parse_data_filters(function_name: str) -> Tuple[str, str]:
    """
    Parse the function name and create the data filters used in the query (and function definition)

    Parameters
    ----------
    function_name: str
        Name of the VBA function, e.g. "STRATODEM_HOUSEHOLDS_WITH_AGE_BETWEEN_FOR_METRO"

    Returns
    -------
    str, str
        Data filters, Data dim in function definition
    """
    data_filters = []
    data_params = []
    re_matches = re.search("(.+?)(?:_WITH)", function_name)

    if re_matches is None:
        return '', ''

    function_name = function_name[len(re_matches.group(1)) + 1:]
    while len(function_name) > 1:
        re_matches = re.search("(?:WITH_)(.+?(?:_).+?)(?:_)", function_name)
        if re_matches is None:
            break
        substring = re_matches.group(1)
        filter_param = substring.split('_')
        data_filters.append(
            map_filter_type_to_filter_dim[filter_param[1]].replace("XXX", filter_param[0]))
        data_params.append(
            map_filter_type_to_filter_template[filter_param[1]].replace("XXX", filter_param[0]))
        function_name = function_name[len(re_matches.group(0)):]

    return ''.join(data_params), ''.join(data_filters)


def parse_geolevel(function_name: str) -> Tuple[str, str]:
    """
    Parse the function name to determine the geographic filters and geographic variable definitions

    Parameters
    ----------
    function_name: str
        Name of the VBA function, e.g. "STRATODEM_HOUSEHOLDS_WITH_AGE_BETWEEN_FOR_METRO"

    Returns
    -------
    str, str
        Geographic filters, Geographic dim in function definition
    """
    re_matches = re.search("(?:FOR_).+", function_name)
    geo = re_matches.group(0)
    geo = geo[4:]

    geo_filters = inner_geo_filters[geo]
    geo_dim = outer_geo_function_dim[geo]

    return geo_filters, geo_dim


def parse_function_name_to_function_info(function_name: str) -> StratoFunction:
    """
    Pull the StratoFunction definition associated with the given function name

    Parameters
    ----------
    function_name: str
        Name of the VBA function, e.g. "STRATODEM_HOUSEHOLDS_WITH_AGE_BETWEEN_FOR_METRO"

    Returns
    -------
    StratoFunction
    """
    re_matches = re.search("(?:STRATODEM_)(.*?)(?:_WITH|_FOR)", function_name)
    function_topic = re_matches.group(1)

    return map_function_topic_to_stratofunction[function_topic]


def generate_vba_function_definition(function_name: str) -> str:
    """
    Generate the VBA function definition for a given function name

    Parameters
    ----------
    function_name: str
        Name of the VBA function, e.g. "STRATODEM_HOUSEHOLDS_WITH_AGE_BETWEEN_FOR_METRO"

    Returns
    -------
    str
        VBA function definition

    Examples
    --------
    ```
    generate_vba_function_definition('STRATODEM_HOUSEHOLDS_WITH_AGE_BETWEEN_FOR_METRO')
    ```
    > Returns
    > Public Function STRATODEM_HOUSEHOLDS_WITH_AGE_BETWEEN_FOR_METRO(YEAR_LOW As Integer, YEAR_HIGH As Integer, AGE_LOW as Integer, AGE_HIGH as Integer, METRO_CODE As Long, API_TOKEN As String) As Variant
    >     STRATODEM_HOUSEHOLDS_WITH_AGE_BETWEEN_FOR_METRO=queryHouseholdsIncomeAge( _
    >         YEAR_LOW:=YEAR_LOW, _
    >         YEAR_HIGH:=YEAR_HIGH, _
    >         AGE_LOW:=AGE_LOW, _
    >         AGE_HIGH:=AGE_HIGH, _
    >         INCOME_LOW:=1, _
    >         INCOME_HIGH:=18, _
    >         geoname:="metro", _
    >         geoFilter:=equalToFilter("cbsa",METRO_CODE), _
    >         API_TOKEN:=API_TOKEN)
    End Function

    """
    data_filter = parse_data_filters(function_name)
    function_info = parse_function_name_to_function_info(function_name)
    geo = parse_geolevel(function_name)

    vba_function_definition = f"""
Public Function {function_name}(YEAR_LOW As Integer, YEAR_HIGH As Integer, {data_filter[1]}{geo[1]}, API_TOKEN As String) As Variant
    {function_name}={function_info.function_name}( _
        YEAR_LOW:=YEAR_LOW, _
        YEAR_HIGH:=YEAR_HIGH, _
        {data_filter[0]}"""

    # TODO not a fan of the mutation here
    function_info.params(vba_function_definition)

    vba_function_definition = function_info.vba_function_definition_str

    vba_function_definition += geo[0] + "\t\tAPI_TOKEN:=API_TOKEN)\nEnd Function\n\n"

    return vba_function_definition


STANDARD_LIBRARY_VBA_CODE = """Private Function submitAPIQuery(query As Dictionary, API_TOKEN As String) As Object
    'Query the StratoDem Analytics API

    Dim httpReq As New WinHttp.WinHttpRequest
    Dim apiToken As String
    Dim apiQuery As Dictionary: Set apiQuery = New Dictionary
    Dim apiQueryString As String
    Dim apiResponse As String
    Dim apiResponseObject As Object

    apiQuery.Add "token", API_TOKEN
    apiQuery.Add "query", query
    apiQueryString = JsonConverter.ConvertToJson(apiQuery)

    'POST the API query to the StratoDem Analytics API
    With httpReq
        .Open "POST", "https://api.stratodem.com/api", False
        .SetRequestHeader "Content-type", "application/json"
        .SetRequestHeader "Accept", "application/json"
        .SetTimeouts 60000, 60000, 60000, 60000
        .Send (apiQueryString)

        'Return the API results
        Set apiResponseObject = JsonConverter.ParseJson(.ResponseText)
        If apiResponseObject("success") Then
            Set submitAPIQuery = apiResponseObject
        Else
            MsgBox "API Query Failed: " + apiResponseObject("message") + " " + apiQueryString
            Err.Raise 5, "API Query Failed", apiResponseObject("message")
        End If
    End With
End Function

' ----- ///// FILTERS ///// ------ '
Private Function apiFilter(filterVariable As String, filterType As String, filterValue As Variant) As Dictionary
    ' Helper method to create an API filter
    Dim filterDict As Dictionary: Set filterDict = New Dictionary

    filterDict.Add "filter_variable", filterVariable
    filterDict.Add "filter_type", filterType
    filterDict.Add "filter_value", filterValue

    Set apiFilter = filterDict
End Function

Private Function equalToFilter(filterVariable As String, filterValue As Variant) As Dictionary
    ' Create "equal to" filter
    Set equalToFilter = apiFilter(filterVariable, "eq", filterValue)
End Function

Private Function notEqualToFilter(filterVariable As String, filterValue As Variant) As Dictionary
    ' Create "not equal to" filter
    Set notEqualToFilter = apiFilter(filterVariable, "ne", filterValue)
End Function

Private Function inFilter(filterVariable As String, filterValue As Variant) As Dictionary
    ' Create "in" filter
    Set inFilter = apiFilter(filterVariable, "in", filterValue)
End Function

Private Function notInFilter(filterVariable As String, filterValue As Variant) As Dictionary
    ' Create "not in" filter
    Set notInFilter = apiFilter(filterVariable, "nin", filterValue)
End Function

Private Function greaterThanFilter(filterVariable As String, filterValue As Variant) As Dictionary
    ' Create "greater than" filter
    Set greaterThanFilter = apiFilter(filterVariable, "gt", filterValue)
End Function

Private Function greaterThanOrEqualToFilter(filterVariable As String, filterValue As Variant) As Dictionary
    ' Create "greater than or equal to" filter
    Set greaterThanOrEqualToFilter = apiFilter(filterVariable, "ge", filterValue)
End Function

Private Function lessThanFilter(filterVariable As String, filterValue As Variant) As Dictionary
    ' Create "less than" filter
    Set lessThanFilter = apiFilter(filterVariable, "lt", filterValue)
End Function

Private Function lessThanOrEqualToFilter(filterVariable As String, filterValue As Variant) As Dictionary
    ' Create "less than or equal to" filter
    Set lessThanOrEqualToFilter = apiFilter(filterVariable, "le", filterValue)
End Function

Private Function betweenFilter(filterVariable As String, filterValue As Variant) As Dictionary
    ' Create "between" filter (a <= x <= b)
    Set betweenFilter = apiFilter(filterVariable, "between", filterValue)
End Function

Private Function drivetimeFilter(LATITUDE As Double, LONGITUDE As Double, minutes As Integer)
    ' Create drivetime filter (within minutes of latitude-longitude pair)
    Dim dtValue As Dictionary: Set dtValue = New Dictionary

    dtValue.Add "latitude", LATITUDE
    dtValue.Add "longitude", LONGITUDE
    dtValue.Add "minutes", minutes

    Set drivetimeFilter = apiFilter("", "drivetime", dtValue)
End Function

Private Function mileRadiusFilter(LATITUDE As Double, LONGITUDE As Double, MILES As Double)
    ' Create mile radius filter (within miles of latitude-longitude pair)
    Dim mrValue As Dictionary: Set mrValue = New Dictionary

    mrValue.Add "latitude", LATITUDE
    mrValue.Add "longitude", LONGITUDE
    mrValue.Add "miles", MILES

    Set mileRadiusFilter = apiFilter("", "mile_radius", mrValue)
End Function

' ----- ///// AGGREGATIONS ///// ------ '
Function apiAggregation(aggregationFunc As String, variableName As String) As Dictionary
    ' Helper method to create an API aggregation
    Dim agg As Dictionary: Set agg = New Dictionary

    agg.Add "aggregation_func", aggregationFunc
    agg.Add "variable_name", variableName

    Set apiAggregation = agg
End Function

Function sumAggregation(variableName As String) As Dictionary
    ' Create a "sum" aggregation
    Set sumAggregation = apiAggregation("sum", variableName)
End Function

Function meanAggregation(variableName As String) As Dictionary
    ' Create a "mean" aggregation
    Set meanAggregation = apiAggregation("mean", variableName)
End Function

' ----- ///// QUERY STRUCTURES ///// ------ '
Function apiQueryParameters(table As String, dataFields As Variant, dataFilters As Variant, _
                            Optional aggregations As Variant, Optional groupby As Variant, _
                            Optional order As Variant, Optional queryType As String = "COUNT", _
                            Optional join As Variant, Optional joinOn As Variant, _
                            Optional LATITUDE As Double, Optional LONGITUDE As Double, _
                            Optional medianVariableName As String, Optional meanVariableName As String) As Dictionary
    ' Structure apiQueryParameters for submitting to the StratoDem Analytics API
    Dim queryParams As Dictionary: Set queryParams = New Dictionary

    queryParams.Add "table", table
    queryParams.Add "query_type", queryType
    queryParams.Add "data_fields", dataFields
    queryParams.Add "data_filters", dataFilters

    If IsMissing(aggregations) Then
        queryParams.Add "aggregations", New Collection
    Else
        queryParams.Add "aggregations", aggregations
    End If
    If IsMissing(groupby) Then
        queryParams.Add "groupby", New Collection
    Else
        queryParams.Add "groupby", groupby
    End If
    If IsMissing(order) Then
        queryParams.Add "order", New Collection
    Else
        queryParams.Add "order", order
    End If
    If Not IsMissing(join) Then
        queryParams.Add "join", join
    End If
    If Not IsMissing(joinOn) Then
        queryParams.Add "on", joinOn
    End If
    If Not IsMissing(LATITUDE) Then
        queryParams.Add "latitude", LATITUDE
    End If
    If Not IsMissing(LONGITUDE) Then
        queryParams.Add "longitude", LONGITUDE
    End If

    queryParams.Add "median_variable_name", medianVariableName
    queryParams.Add "mean_variable_name", meanVariableName

    Set apiQueryParameters = queryParams
End Function

Function medianQueryParameters(table As String, dataFields As Variant, dataFilters As Variant, _
                               medianVariableName As String, _
                               Optional aggregations As Variant, Optional groupby As Variant, _
                               Optional order As Variant, Optional join As Variant, Optional joinOn As Variant) As Dictionary
    ' Structure a median query for submitting to the StratoDem Analytics API
    Set medianQueryParameters = apiQueryParameters(table, _
                                                   dataFields, _
                                                   dataFilters, _
                                                   aggregations:=aggregations, _
                                                   groupby:=groupby, _
                                                   order:=order, _
                                                   queryType:="MEDIAN", _
                                                   join:=join, _
                                                   joinOn:=joinOn, _
                                                   medianVariableName:=medianVariableName)
End Function

Function meanQueryParameters(table As String, dataFields As Variant, dataFilters As Variant, _
                             meanVariableName As String, _
                             Optional aggregations As Variant, Optional groupby As Variant, _
                             Optional order As Variant, Optional join As Variant, Optional joinOn As Variant) As Dictionary
    ' Structure a mean query for submitting to the StratoDem Analytics API
    Set meanQueryParameters = apiQueryParameters(table, _
                                                 dataFields, _
                                                 dataFilters, _
                                                 aggregations:=aggregations, _
                                                 groupby:=groupby, _
                                                 order:=order, _
                                                 queryType:="MEAN", _
                                                 join:=join, _
                                                 joinOn:=joinOn, _
                                                 meanVariableName:=meanVariableName)
End Function

Function geocoderQueryParameters(table As String, LATITUDE As Double, LONGITUDE As Double, dataFields As Variant) As Dictionary
    ' Structure a geocoder query for submitting to the StratoDem Analytics API
    Set geocoderQueryParameters = apiQueryParameters(table, _
                                                     dataFields:=dataFields, _
                                                     LATITUDE:=LATITUDE, _
                                                     LONGITUDE:=LONGITUDE, _
                                                     dataFilters:=Array(), _
                                                     queryType:="GEOCODER")
End Function

Function renameVariable(original As String, renamed As String) As Dictionary
    ' Rename a variable from original to renamed in the database query
    Dim renameDict As Dictionary: Set renameDict = New Dictionary

    renameDict.Add original, renamed

    Set renameVariable = renameDict
End Function

Function joinOnStructure(left As Variant, right As Variant) As Dictionary
    ' Create the correct joining structure for queries
    Dim joinOnDict As Dictionary: Set joinOnDict = New Dictionary

    joinOnDict.Add "left", left
    joinOnDict.Add "right", right
    Set joinOnStructure = joinOnDict
End Function

' ----- ///// UTILITIES ///// ----- '
Private Function geolevelToGeocol(GEOLEVEL As String) As String
    If GEOLEVEL = "US" Then
        geolevelToGeocol = ""
    ElseIf GEOLEVEL = "GEOID2" Then
        geolevelToGeocol = "geoid2"
    ElseIf GEOLEVEL = "GEOID5" Then
        geolevelToGeocol = "geoid5"
    ElseIf GEOLEVEL = "METRO" Then
        geolevelToGeocol = "cbsa"
    ElseIf GEOLEVEL = "ZIP" Then
        geolevelToGeocol = "zip"
    ElseIf GEOLEVEL = "GEOID11" Then
        geolevelToGeocol = "geoid11"
    Else
        Err.Raise 5, "geolevelToGeocol", "Failed to map GEOLEVEL " & GEOLEVEL
    End If
End Function

Private Function geolevelToGeoname(GEOLEVEL As String) As String
    If GEOLEVEL = "US" Then
        geolevelToGeoname = ""
    ElseIf GEOLEVEL = "GEOID2" Then
        geolevelToGeoname = "state"
    ElseIf GEOLEVEL = "GEOID5" Then
        geolevelToGeoname = "county"
    ElseIf GEOLEVEL = "METRO" Then
        geolevelToGeoname = "metro"
    ElseIf GEOLEVEL = "ZIP" Then
        geolevelToGeoname = "zip"
    ElseIf GEOLEVEL = "GEOID11" Then
        geolevelToGeoname = "tract"
    Else
        Err.Raise 5, "geolevelToGeoname", "Failed to map GEOLEVEL " & GEOLEVEL
    End If
End Function
"""

if __name__ == '__main__':
    vba_script = """
' StratoDem Analytics Excel Add-in for User-Defined Functions
' (c) StratoDem Analytics, 2019-
' Questions? Email team@stratodem.com
"""

    for function_ in map_function_topic_to_stratofunction.values():
        for query in function_.queries:
            vba_script += generate_vba_function_definition(query)

        vba_script += function_.function_string

    vba_script += STANDARD_LIBRARY_VBA_CODE

    with open('Strato_Excel_Add_In.txt', 'w') as f:
        f.write(vba_script)
