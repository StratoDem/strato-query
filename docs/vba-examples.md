## StratoDem Analytics for Excel in VBA
Tools to help query the StratoDem Analytics API for economic and geo-demographic data using VBA in Excel

[Back to main page](/)

## Table of contents
- [Installation and usage](#installation-and-usage)
  - [Running the template the first time](#first-run)
  - [Editting the template to add a new query](#adding-a-query)
- [Sample queries](#sample-queries)
  - [Median household income for 80+ households across the US, by year](#median-household-income-for-80-households-across-the-us-by-year)
  - [Population within five miles of latitude-longitude pair](#population-within-five-miles-of-latitude-longitude-pair)
- [Using Blaise ML to generate queries](#using-blaise-ml-to-generate-queries)

### [Installation and usage](#installation-and-usage)

#### [Running the template the first time](#first-run)
1. Download API template ([download here](https://github.com/StratoDem/strato-query/raw/master/StratoDem_API_Template.xlsm))
2. Get an API token and place in the correct cell (`Configuration!B5`)
3. Select one to three buffers
4. Enter locations in the bottom section
5. Click RUN QUERIES

[How do I create a new API token or find an existing token? &rarr;](https://academy.stratodem.com/article/82-creating-and-managing-api-tokens)

<img src="assets/images/Excel_API_template.png" alt="StratoDem Analytics API token in Excel" />

#### [Editting the template to add a new query](#adding-a-query)
1. Download API template (here → add link)
2. Get an API token and place in the correct cell
3. Enable Developer tab in Excel (we’ll come back here in a bit)
4. Open Portfolio
5. Load in a custom portfolio defined with mile radius markets (here’s how to do that → )
6. Ask Blaise “Which markets have the highest median household income for 80+ households in 2019?”
7. Open “Adjust the question” drawer to open the options drawer
8. Click “View API query”
9. Click on the Excel VBA tab
10. The code here includes the query objects necessary to replicate the query for each market definition in the entire portfolio. We’re only going to use one of them for now.
11. Open Visual Basic editor
12. We’re going to modify the `writeLocationData` function to add a column for median household income for 80+ households in 2019
13. Create a new function (ours will be called `querySeniorMedianHouseholdIncome`)
14. From the Portfolio app, copy the first query section into that new function
15. Edit:
    1. The year filter to be the year passed in as an argument
    2. The mile radius filter to use `latitude`, `longitude`, and `mileRadius` passed in as arguments
16. To have the function return a value, we need to add one final line to the end of the function:
 
    `querySeniorMedianHouseholdIncome = dataResults("data")(1)("median_val")` 
    
    where `median_val` is whatever the metric name returned is
17. Add a code block to the `writeLocationData` that calls our new querySeniorMedianHouseholdIncome function and writes the data (make sure to use a new column index number)
    ```VBA
    ' Write senior median household income (age 80+)
    Worksheets("Output").Cells(firstLocationRowNumber, 13).Value = querySeniorMedianHouseholdIncome(latitude, longitude, radius1, 2019)
    Worksheets("Output").Cells(firstLocationRowNumber + 1, 13).Value = querySeniorMedianHouseholdIncome(latitude, longitude, radius2, 2019)
    Worksheets("Output").Cells(firstLocationRowNumber + 2, 13).Value = querySeniorMedianHouseholdIncome(latitude, longitude, radius3, 2019)
    ```
18. Add a column name writer to `writeColumnMetadata`:

    `Worksheets("Output").Cells(1, 13).Value = "Median household income 80+ households (2019)"  ' M1`
    
19. Now we need to add one more row for the associated metro.
20. Change the geographic coverage level in Portfolio to “Metro”
21. Open up the View API query dialog again and we’ll copy the code from the Excel VBA tab again
22. Open up the Visual Basic Editor
23. Create a new function (we’ll call it `querySeniorMedianHouseholdIncomeMetro`) that we’ll use to get the metro data
24. From the Portfolio app, copy the first query section into that new VBA Function
25. Edit:
    1. The year filter to be the year passed in as an argument
    2. Add one more filter: 
        
        `equalToFilter(filterVariable:=”cbsa”, filterValue:=cbsaCode)`
        
        This makes sure we’re only getting data for the target metro area
26. To have the function return a value, we need to add one final line to the end of the function:
 
    `querySeniorMedianHouseholdIncomeMetro = dataResults("data")(1)("median_val")` 
    
    where `median_val` is whatever the metric name returned is
27. Add one more line of code to the “writeLocationData” below where we wrote our previous new query calls for mile-radius-defined market areas:
 
    `Worksheets("Output").Cells(firstLocationRowNumber + 3, 13).Value = querySeniorMedianHouseholdIncomeMetro(cbsaCode, 2019)`

28. Run the query!


### [Sample queries](#sample-queries)

#### [Median household income for 80+ households across the US, by year](#median-household-income-for-80-households-across-the-us-by-year)
```VBA
' Finds median household income in the US for those 80+ from 2010 to 2013
Dim medianHHIQuery As Dictionary

Set medianHHIQuery = medianQueryParameters( _
    table:="incomeforecast_us_annual_income_group_age", _
    dataFields:=Array("year", renameVariable(original:="median_value", renamed:="median_income")), _
    dataFilters:=Array( _
        greaterThanFilter(filterVariable:="age_g", filterValue:=17), _
        betweenFilter(filterVariable:="year", filterValue:=Array(2010, 2013))), _
    groupby:=Array("year"), _
    medianVariableName:="income_g", _
    aggregations:=Array())

' Write the results to "US_median_household_income" (note that this sheet will need to exist first)
Call writeToSheet(results:=submitAPIQuery(medianHHIQuery), sheetName:="US_median_household_income")
```

Output:

<img src="assets/images/us_median_hhi_80plus.png" alt="80+ median household income in Excel from the StratoDem Analytics API" />

### [Population within five miles of latitude-longitude pair](#population-within-five-miles-of-latitude-longitude-pair)
```VBA
' Gets population within five miles of 40.7589, -73.9937
Dim populationQuery As Dictionary

Set populationQuery = apiQueryParameters( _
    table:="populationforecast_tract_annual_population", _
    dataFields:=Array("year", renameVariable(original:="population", renamed:="population_within_5_miles")), _
    dataFilters:=Array( _
        mileRadiusFilter(latitude:=40.7589, longitude:=-73.9937, miles:=5), _
        betweenFilter(filterVariable:="year", filterValue:=Array(2010, 2020))), _
    groupby:=Array("year"), _
    aggregations:=Array(sumAggregation(variableName:="population")))

' Write the results to "Population_within_five_miles" (note that this sheet will need to exist first)
Call writeToSheet(results:=submitAPIQuery(populationQuery), sheetName:="Population_within_five_miles")
```

Output:

<img src="assets/images/population_within_five_miles_excel.png" alt="Population within five miles of Times Square in Excel from the StratoDem Analytics API" />

## [Using Blaise ML to generate queries](#using-blaise-ml-to-generate-queries)
Blaise ML by StratoDem Analytics is embedded in all StratoDem Analytics applications. One feature that Blaise ML supports is
generating the code for API queries from a natural language question in the [Portfolio application on clients.stratodem.com](https://clients.stratodem.com/dash/?id=marketscorecard).

To generate the code in VBA, just:
1. Type in the question to the text bar at the top of the application
2. Click **Adjust the question** to open the query adjustment drawer
3. Click **View API query** above the question in the drawer
4. Switch to the **VBA** tab and copy the generated API query/queries into your favorite R editor

#### Find the estimated household count by metro for adults ages 80+ and net worth of at least $100,000 in 2020  
<img src="assets/images/VBA_example_query.gif" alt="Using Blaise ML to create a sample query in VBA" />
