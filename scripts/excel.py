import itertools
import re
scripts=[]
s=""

'''
Naming Conventions

query = 1 specific type of query for the API -> STRATODEM_HOUSEHOLDS_WITH_INCOME_BETWEEN_FOR_METRO

function = multiple different variations for different 
input variables and filters of queries -> queryHouseholdsIncomeAge

 many queries -> 1 function

'''

#Values for variables to default to give broad range
default_values={
    'AGE':'\t\tAGE_LOW:=1, _ \n\t\tAGE_HIGH:=18, _\n',
    'INCOME':'\t\tINCOME_LOW:=1, _ \n\t\tINCOME_HIGH:=18, _\n'
}


#List of all supported filters and their templates
filters={
    'BETWEEN':'XXX_LOW as Integer, XXX_HIGH as Integer, '
}

#Templates for all supported filters for the paramaters for functions
params={
    'BETWEEN':'\t\tXXX_LOW:=XXX_LOW, _\n\t\tXXX_HIGH:=XXX_HIGH, _\n'
} 

#List of all supported geo locations 
upper_geo={'METRO':'METRO_CODE As Long',
     #'STATE': 'GEOID2',
     'COUNTY': 'COUNTY_CODE As Long',
     #'US':'US',
     #"MICRO":'micro',
     #'ZIP':"zip",
     #'TRACT': 'GEOID11',
     'MILE_RADIUS':"LATITUDE As Double, LONGITUDE As Double, MILES As Double"
     #'DRIVE_TIME':'drive_time'
}


#Geo templates for function parameters
lower_geo={
    'METRO':"\t\tgeoname:=\"metro\", _\n\t\tgeoFilter:=equalToFilter(\"cbsa\",METRO_CODE), _\n",
    #'STATE':'LOL',
    'COUNTY': "\t\tgeoname:=\"county\", _\n\t\tgeoFilter:=equalToFilter(\"geoid5\",COUNTY_CODE), _\n",
    #"US":"Still gotta do",
    #"MICRO":"WILL FINISH",
    #"ZIP":"I PROMISE",
    #"TRACT":"working on replicating the excel example first",
    "MILE_RADIUS":"\t\tgeoname:=\"tract\", _\n\t\tgeoFilter:=mileRadiusFilter(LATITUDE:=LATITUDE,LONGITUDE:=LONGITUDE, MILES:=MILES), _\n"
    #"DRIVE_TIME": "Okay last one"
}

#Template for VBA QUERY
template="QUERY_NAME(FILTER_PARAMS, GEO_PARAMS, API_TOKEN As String) As Variant\nQUERY_NAME = FUNCTION"

#Template for end of VBA function
helper_function_template='''   
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

class stratofunction:
    #Creates all possible combinations of queries with given input variables
    def __init__(self,user_variables,function_title):
        self.user_variables=user_variables
        self.queries=[]
        filters_and_data=[]
        combos=[]
        for _filter in filters.keys():
            for variable in self.user_variables:
                filters_and_data.append(f"WITH_{variable}_{_filter}_")
        for i in range(1,len(self.user_variables)+1):
            combos.append(list(itertools.combinations(filters_and_data,i)))
        for combo in combos:
            for variable in combo:
                query=''.join(variable)
                for geo in upper_geo.keys():
                    self.queries.append(f"STRATODEM_{function_title}_{query}FOR_{geo}")
        for geo in upper_geo.keys():
            self.queries.append(f"STRATODEM_{function_title}_FOR_{geo}")
    
    def params(self,query):
        for variable in self.user_variables:
            if variable not in query:
                query=query+default_values[variable]
        self.s=query

class households(stratofunction):
    def __init__(self):
        super().__init__(['AGE','INCOME'],'HOUSEHOLDS')
        self.s=""
        self.function_name="queryHouseholdsIncomeAge"
        self.function_string='''Public Function queryHouseholdsIncomeAge(YEAR_LOW As Integer, YEAR_HIGH As Integer, INCOME_LOW As Integer, INCOME_HIGH As Integer, AGE_LOW As Integer, AGE_HIGH As Integer, geoname As String, geoFilter As Dictionary, API_TOKEN As String) As Variant
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
        self.function_string=self.function_string.replace("XXX",self.function_name)


class median_household_income(stratofunction):
    def __init__(self):
        super().__init__(['AGE',],"MEDIAN_HOUSEHOLD_INCOME")
        self.s=""
        self.function_name="queryMedianIncomeAge"
        self.function_string='''Public Function queryMedianIncomeAge(YEAR_LOW As Integer, YEAR_HIGH As Integer, AGE_LOW As Integer, AGE_HIGH As Integer, geoname As String, geoFilter As Dictionary, API_TOKEN As String) As Variant
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
        self.function_string=self.function_string.replace("XXX",self.function_name)




#List of all supported function types
stratodem_functions={
    'HOUSEHOLDS':households(),
    'MEDIAN_HOUSEHOLD_INCOME':median_household_income()
}


def data_filterParser(s):
    data_filters=[]
    data_params=[]
    x=re.search("(.+?)(?:_WITH)",s)
    if (x is None):
        return['','']
    s=s[len(x.group(1))+1:]
    while(len(s)>1):
        x=re.search("(?:WITH_)(.+?(?:_).+?)(?:_)",s)
        if (x is None):
            break
        substring=x.group(1)
        filter_param=substring.split('_')
        data_filters.append(filters[filter_param[1]].replace("XXX",filter_param[0]))
        data_params.append(params[filter_param[1]].replace("XXX",filter_param[0]))
        s=s[len(x.group(0)):]
    return [''.join(data_params),''.join(data_filters)]

def geoParser(s):
    x=re.search("(?:FOR_).+",s)
    geo=x.group(0)
    geo=geo[4:]
    return [lower_geo[geo],upper_geo[geo]]

def functionParser(s):
    x=re.search("(?:STRATODEM_)(.*?)(?:_WITH|_FOR)",s)
    function=x.group(1)    
    return stratodem_functions[function]
    
def stringParser(s):
    query="Public Function "+s
    data_filter=data_filterParser(s)
    query=query+"(YEAR_LOW As Integer, YEAR_HIGH as Integer, " + data_filter[1]
    function_info=functionParser(s)
    geo=geoParser(s)
    query=query+geo[1]+", API_TOKEN As String) As Variant\n"
    query=query+"\t"+s+"="+function_info.function_name+"( _\n\t\tYEAR_LOW:=YEAR_LOW, _ \n\t\tYEAR_HIGH:=YEAR_HIGH, _\n"+data_filter[0]
    function_info.params(query)
    query=function_info.s
    query=query +geo[0] + "\t\tAPI_TOKEN:=API_TOKEN)\nEnd Function\n\n"
    return query

VBA_Script=""

for x in stratodem_functions.values():
    for query in x.queries:
        VBA_Script=VBA_Script+stringParser(query)
    VBA_Script=VBA_Script+x.function_string
VBA_Script=VBA_Script+'''Private Function submitAPIQuery(query As Dictionary, API_TOKEN As String) As Object
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

'''
f=open("Strato_Excel_Add_In.txt","w+")
f.write(VBA_Script)
f.close()

