# Changelog for strato-query

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## [3.10.3] - 2024-05-07
### Changes
- Updated Stratodem API Token due to unwhitelisted Token Error

## [3.10.2] - 2023-02-28
### Changes
- Changes the jobsAPI URLs to update with the new environment variable as well

## [3.10.1] - 2023-02-14
### Changes
- Changes the API URL to make it configurable using an environment variable

## [3.10.0] - 2021-05-03
### Adds
- Adds support for using saved custom markets with the jobs API
- Adds docstrings to methods in the SDJobRunner class

## [3.9.9] - 2021-04-23
### Changes
- `chunksize` may now be set globally for multiple queries with configuration variable in `api_query.api_configuration['chunksize']`
- `timeout` may now be set globally for multiple queries with configuration variable in `api_query.api_configuration['timeout']`

## [3.9.8] - 2021-02-24
### Adds
- Adds new allowed buffer values

## [3.9.7] - 2021-02-23
### Changes
- Restores test that was commented out

### Fixes
- Fixes `sites` value when it is not received as part of a query by setting it to an empty list

## [3.9.6] - 2021-02-18
### Adds
- Adds support for site addresses to `SDJobRunner`

## [3.9.5] - 2020-09-29
### Adds
- Adds support for `buffers` to `SDJobRunner` for portfolio queries

## [3.9.4] - 2020-09-29
### Adds
- Adds optional logging to `SDJobRunner` to track job creation and polling

## [3.9.3] - 2020-09-29
### Fixes
- Default `geoid_list` to `[]` instead of `None` to API service

## [3.9.2] - 2020-09-29
### Fixes
- (internal) Allows for `geolevel` to be `None` if specifying a `portfolio_id` in `SDJobRunner`

## [3.9.1] - 2020-09-24
### Fixes
- (internal) Adds `long_description` to `setup.py` to display description on PyPI

## [3.9.0] - 2020-09-24
### Adds
- Adds `SDJobRunner`, a utility object that allows for querying StratoDem Analytics models by creating jobs
```python
from strato_query import SDJobRunner, authenticate_to_api

authenticate_to_api('my-api-token')

# This loads a query set defined in the client portal for the Boston and Austin MSAs
df = SDJobRunner().load_df_from_job_pipeline(
    model_id='5ADyVKql',
    geolevel='METRO',
    geoid_list=[14454, 12420]
)
```

## [3.8.1] - 2020-09-11
### Adds
- Adds support for `walktime_simple` and `walktime_destination_simple`

## [3.8.0] - 2020-07-31
### Adds
- Adds a new arg, `time_between_chunks`, to the `query_api_multiple` method
  By default, this arg is set to `None`, which will preserve existing behavior for unchanged queries. When given a value, the method will sleep for the specified time after each chunk is POSTed, and will continue to do so until all chunks have been submitted. The method will not sleep after the final chunk

## Related issues
- [121](https://github.com/StratoDem/strato-query/issues/121)

## [3.7.0] - 2019-05-15
### Adds
- Adds new query param classes:
  - `APIMilesDistanceQueryParams`
  - `APIDrivingDistanceQueryParams`
  - `APIWalkingDistanceQueryParams`

## Related issues
- [109](https://github.com/StratoDem/strato-query/issues/109)

## [3.6.2] - 2019-05-08
### Changes
- Checks specifically for a 520 error and immediately raises a timeout

## Related issues
- [107](https://github.com/StratoDem/strato-query/issues/107)

## [3.6.1] - 2019-05-04
### Changes
- Changes the error raised when the max number of query retries has been exceeded so it more clearly alerts API users that a timeout has occurred.

## Related issues
- [104](https://github.com/StratoDem/strato-query/issues/104)

## [3.6.0] - 2019-02-07
### Changes
- `SDAPIQuery.query_api_multiple` now chunks queries into 500-size batches by default, configurable with `chunksize`

## Related issues
- [94](https://github.com/StratoDem/strato-query/issues/94)

## [3.5.0] - 2019-11-13
### Changes
- Updates the pretty print behavior to account for new buffer filters
- Updates the R filters for new filter types

## Related issues
- [88](https://github.com/StratoDem/strato-query/issues/88)

## [3.4.0] - 2019-11-06
### Adds
- Adds new `detailed_type` option to `IntersectsFilter`. It now supports:
    - `'intersects'` (simple intersection filtering)
    - `'intersects_weighted'` (ability to create weighted polygon results)

## Related issues
- [85](https://github.com/StratoDem/strato-query/issues/85)

## [3.3.0] - 2019-09-18
### Adds
- Adds new buffer types to the `DrivetimeFilter`. It now supports:
    - `'drivetime'`
    - `'drivetime_simple'`
    - `'drivetime_unweighted'`
    - `'drivetime_destination'`
    - `'drivetime_destination_simple'`
    - `'drivetime_destination_unweighted'`
- Adds a `WalktimeFilter` which supports the following types:
    - `'walktime'`
    - `'walktime_unweighted'`
    - `'walktime_destination'`
    - `'walktime_destination_unweighted'`
- Adds `detailed_type` as a new optional argument to `OverlapsDrivetimeFilter` which allows:
    - `'overlaps_drivetime'`
    - `'overlaps_drivetime_destination'`
- Adds `detailed_type` as a new optional argument to `OverlapsWalktimeFilter` which allows:
    - `'overlaps_walktime'`
    - `'overlaps_walktime_destination'`

## Related issues
- [69](https://github.com/StratoDem/strato-query/issues/69)

## [3.2.0] - 2019-09-10
### Adds
- Adds new query param classes
    - `APIPureShapeQueryParams`
    - `APIPureShapeUnionQueryParams`
- Adds examples of new query params classes

## Related issues
- [69](https://github.com/StratoDem/strato-query/issues/69)

## [3.1.0] - 2019-09-10
### Adds
- Adds new filter types for overlaps. Each one takes the data needed to create the shape used to check against the specified geometry column
    - `OverlapsMileRadiusFilter`
    - `OverlapsDrivetimeFilter`
    - `OverlapsWalktimeFilter`

## Related issues
- [69](https://github.com/StratoDem/strato-query/issues/69)

## [3.0.2] - 2019-09-05
### Fixes
- Fixes broken links to examples in documentation. Now links to new docs site at code.stratodem.com

## [3.0.1] - 2019-08-26
### Changes
- Failed API queries no longer include API token value in the error message (replaced by `**********`)

## [3.0.0] - 2019-08-22
### Changes
- **Breaking** Renames filters to full words in Python package. E.g., `EqFilter` --> `EqualToFilter`
- Arguments no longer must be `tuple`s, but can also be `list`s :tada:
- `data_filters` argument for `APIQueryParams` may be an iterable of `BaseFilter` objects, instead of only `dict`s
- `BaseAggregation` and `SumAggregation` added to handle aggregations instead of relying on arbitrary `dict`s
- `aggregations` argument for `APIQueryParams` may be an iterable of `BaseAggregation` objects, instead of only `dict`s
- Renames `BaseAPIQuery` --> `SDAPIQuery`
- New authentication method to support environment variable at `STRATODEM_API_TOKEN` or `authenticate_to_api('my-api-token')`
- New documentation site with Python, R, Shell, and VBA examples :tada:

```python
from strato_query import SDAPIQuery, APIQueryParams, EqualToFilter, LessThanFilter
from strato_query.authentication import authenticate_to_api

authenticate_to_api('my-api-token')

df = SDAPIQuery.query_api_df(
    query_params=APIQueryParams(
        query_type='COUNT',
        table='populationforecast_metro_annual_population',
        data_fields=('year', 'cbsa', {'population': 'population'}),
        data_filters=(
            LessThanFilter(var='year', val=2015),
            EqualToFilter(var='cbsa', val=14454),
        ),
        aggregations=(dict(aggregation_func='sum', variable_name='population'),),
        groupby=('cbsa', 'year'),
        order=('year',),
        join=APIQueryParams(
            query_type='AREA',
            table='geocookbook_metro_na_shapes_full',
            data_fields=('cbsa', 'area', 'name'),
            data_filters=(EqualToFilter(var='cbsa', val=14454),),
            groupby=('cbsa', 'name'),
            aggregations=(),
            on=dict(left=('cbsa',), right=('cbsa',)),
        )
    )
)
```

## [2.11.1] - 2019-05-16
### Fixes
- Fixes an incorrect assertion statement in the `submit_query` method

### Related issues:
- [#53](https://github.com/StratoDem/strato-query/issues/53)

## [2.11.0] - 2019-05-07
### Adds
- Adds a new filter, `IntersectsFilter`, for querying all geoids whose geometries intersect with the given bounding geometry

### Related issues:
- [#50](https://github.com/StratoDem/strato-query/issues/50)

## [2.10.2] - 2019-04-22
### Changes
- Changes the pretty print methods in the `APIQueryParams` class so they can handle pretty printing for all query param classes
- Removes the pretty print methods from the `APICalculationQueryParams` class

### Related issues:
- [#48](https://github.com/StratoDem/strato-query/issues/48)

## [2.10.1] - 2019-04-22
### Changes
- Changes default timeout value to 60s

## [2.10.0] - 2019-04-22
### Adds
- Adds the `APICalculationQueryParams` class
- Adds the `APIFilterQueryParams` class

### Related issues:
- [#43](https://github.com/StratoDem/strato-query/issues/43)

## [2.9.0] - 2019-04-17
### Adds
- Adds automatic retries for the POST request if there is a connection issue
- Adds an optional, adjustable `timeout` param to exposed methods
- Adds docstrings to class methods

### Related issues:
- [#39](https://github.com/StratoDem/strato-query/issues/39)

## [2.8.0] - 2019-03-22
### Fixes
- Includes `APIGeoJSONQueryParams` in `__all__` for `base_API_query.py`

### Adds
- Adds `APIGeocoderQueryParams`, which, when called form
  `BaseAPIQuery.query_api_df`, returns a `DataFrame` with the geographic
  information associated with a latitude-longitude pair.

  Example:
  ```python
  from strato_query.base_API_query import BaseAPIQuery, APIGeocoderQueryParams

  BaseAPIQuery.query_api_df(
    query_params=APIGeocoderQueryParams(
        data_fields=('geoid11', 'geoid5',),
        table='geocookbook_tract_na_shapes_full',
        data_filters=(),
        groupby=(),
        aggregations=(),
        latitude=42.983899,
        longitude=-99.306204))
  ```

  ```
         GEOID11  GEOID5
  0  31103975400   31103
  ```

## [2.7.0] - 2019-03-07
### Adds
- Adds `APIGeoJSONQueryParams`, which, when called from
  `BaseAPIQuery.query_api_json`, returns a GeoJSON `FeatureCollection`
  with data optionally added to the `properties` field in each GeoJSON
  `Feature`.

  ```python
  from strato_query.base_API_query import BaseAPIQuery, APIGeoJSONQueryParams, APIQueryParams

  BaseAPIQuery.query_api_json(
    query_params=APIGeoJSONQueryParams(
        data_fields=('geoid2', 'geometry'),
        table='geocookbook_state_na_shapes_simplified',
        properties=('geoid2', 'population'),
        data_filters=(
            {'filter_type': 'eq', 'filter_variable': 'geoid2', 'filter_value': 25},
        ),
        aggregations=(),
        groupby=(),
        join=APIQueryParams(
            table='populationforecast_state_annual_population',
            data_fields=({'geoid2': 'geoid2_pop'}, 'population'),
            aggregations=(),
            data_filters=(
                {'filter_type': 'eq', 'filter_variable': 'year', 'filter_value': 2019},
            ),
            groupby=(),
            on=dict(left=['geoid2'], right=['geoid2_pop'])
        ),
    ))
  ```

  ```json
  {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "MultiPolygon",
          "coordinates": [[[[-70.23405, 41.28565], [-70.21504, 41.27958], [-70.21171, 41.27565], [-70.20173, 41.27654], [-70.19389, 41.28029], [-70.19175, 41.28655], [-70.19579, 41.29065], [-70.2022, 41.28797], [-70.20569, 41.29125], [-70.19911, 41.29619], [-70.18699, 41.29451], [-70.12446, 41.29385], [-70.10961, 41.29538], [-70.10441, 41.29733], [-70.08207, 41.29909], [-70.06256, 41.30873], [-70.04609, 41.32165], [-70.03133, 41.33933], [-70.02442, 41.36062], [-70.02403, 41.36861], [-70.03464, 41.37899], [-70.04559, 41.3836], [-70.04274, 41.38931], [-70.02038, 41.36901], [-69.96028, 41.27873], [-69.96018, 41.26455], [-69.96413, 41.25538], [-69.97498, 41.24653], [-70.0016, 41.23992], [-70.01522, 41.23796], [-70.05318, 41.24403], [-70.08349, 41.24477], [-70.10049, 41.24055], [-70.11867, 41.24235], [-70.17036, 41.25743], [-70.22134, 41.27704], [-70.23405, 41.28565]]], [[[-70.27665, 41.31128], [-70.26295, 41.31145], [-70.24655, 41.30619], [-70.23982, 41.29582], [-70.24767, 41.28864], [-70.25254, 41.29303], [-70.26862, 41.30177], [-70.27665, 41.31128]]], [[[-70.30897, 41.33606], [-70.30432, 41.33842], [-70.29203, 41.33779], [-70.29086, 41.33366], [-70.307, 41.33239], [-70.30897, 41.33606]]], [[[-70.8071, 41.45858], [-70.79835, 41.46881], [-70.79245, 41.46929], [-70.78415, 41.47796], [-70.77549, 41.4771], [-70.76799, 41.48779], [-70.7549, 41.49102], [-70.74715, 41.49989], [-70.7376, 41.50426], [-70.73017, 41.50318], [-70.71022, 41.51892], [-70.70252, 41.51964], [-70.69943, 41.51359], [-70.68731, 41.51235], [-70.67828, 41.51733], [-70.67471, 41.51235], [-70.68156, 41.50727], [-70.68989, 41.50453], [-70.69373, 41.50683], [-70.70704, 41.50149], [-70.70454, 41.49681], [-70.71227, 41.49063], [-70.73437, 41.48689], [-70.7472, 41.47781], [-70.75671, 41.47906], [-70.76099, 41.473], [-70.75566, 41.46715], [-70.76113, 41.46111], [-70.76788, 41.45769], [-70.77631, 41.45766], [-70.79039, 41.44653], [-70.8, 41.44617], [-70.8052, 41.45038], [-70.8071, 41.45858]]], [[[-70.83204, 41.2595], [-70.81966, 41.26006], [-70.81415, 41.26228], [-70.80156, 41.25841], [-70.80424, 41.24946], [-70.82551, 41.25228], [-70.83204, 41.2595]]], [[[-70.83595, 41.60252], [-70.82373, 41.59857], [-70.82092, 41.58767], [-70.82191, 41.58284], [-70.83009, 41.58538], [-70.83845, 41.59646], [-70.83595, 41.60252]]], [[[-70.83878, 41.34721], [-70.8338, 41.35339], [-70.81985, 41.35358], [-70.81231, 41.35575], [-70.80029, 41.3538], [-70.78329, 41.34783], [-70.77497, 41.34918], [-70.7689, 41.35325], [-70.75864, 41.36695], [-70.74043, 41.38278], [-70.73698, 41.39153], [-70.73186, 41.3978], [-70.72437, 41.39894], [-70.71971, 41.40466], [-70.71243, 41.40885], [-70.71149, 41.41546], [-70.70656, 41.4192], [-70.70096, 41.43401], [-70.68992, 41.43684], [-70.68688, 41.44133], [-70.67186, 41.44236], [-70.66592, 41.45109], [-70.66508, 41.45623], [-70.65965, 41.46068], [-70.64215, 41.46232], [-70.62002, 41.47459], [-70.60355, 41.48238], [-70.59844, 41.48115], [-70.5958, 41.46873], [-70.59984, 41.46143], [-70.59913, 41.45537], [-70.592, 41.4559], [-70.58368, 41.46071], [-70.57485, 41.46826], [-70.56736, 41.47121], [-70.56328, 41.46913], [-70.55328, 41.45295], [-70.55294, 41.44339], [-70.55559, 41.43088], [-70.54757, 41.41583], [-70.5383, 41.40924], [-70.52858, 41.4051], [-70.51758, 41.40377], [-70.50698, 41.40024], [-70.50237, 41.392], [-70.50131, 41.38539], [-70.49076, 41.38363], [-70.4845, 41.38629], [-70.47169, 41.3962], [-70.47303, 41.40876], [-70.46383, 41.41915], [-70.45043, 41.4207], [-70.44623, 41.39648], [-70.44927, 41.38042], [-70.44826, 41.35365], [-70.45224, 41.34983], [-70.46329, 41.34748], [-70.48243, 41.3484], [-70.49503, 41.34751], [-70.57916, 41.35001], [-70.6488, 41.34697], [-70.69111, 41.3443], [-70.70983, 41.34172], [-70.73325, 41.33623], [-70.74754, 41.32995], [-70.76419, 41.31871], [-70.76801, 41.31196], [-70.76869, 41.3037], [-70.77566, 41.30098], [-70.80208, 41.31421], [-70.81941, 41.32721], [-70.83878, 41.34721]]], [[[-70.84037, 41.45288], [-70.83251, 41.45795], [-70.82059, 41.45851], [-70.80829, 41.44949], [-70.81447, 41.44593], [-70.82288, 41.44531], [-70.83087, 41.44129], [-70.83687, 41.44197], [-70.84156, 41.44913], [-70.84037, 41.45288]]], [[[-70.90479, 41.42775], [-70.90101, 41.43445], [-70.88221, 41.43256], [-70.8803, 41.43797], [-70.86367, 41.44254], [-70.85582, 41.44058], [-70.84856, 41.43284], [-70.86266, 41.42412], [-70.87122, 41.42208], [-70.88937, 41.42263], [-70.90188, 41.42133], [-70.90479, 41.42775]]], [[[-70.94249, 42.32685], [-70.93207, 42.32859], [-70.9225, 42.32639], [-70.92547, 42.31921], [-70.94249, 42.32685]]], [[[-70.95108, 42.28973], [-70.94165, 42.29221], [-70.9357, 42.29652], [-70.93527, 42.3021], [-70.92664, 42.2992], [-70.93531, 42.29193], [-70.93733, 42.28492], [-70.95108, 42.28973]]], [[[-70.94918, 41.41578], [-70.94329, 41.41492], [-70.9411, 41.42174], [-70.93212, 41.42508], [-70.92747, 41.43181], [-70.91976, 41.42526], [-70.92974, 41.41456], [-70.94876, 41.40904], [-70.94918, 41.41578]]], [[[-70.9774, 42.31229], [-70.97039, 42.31624], [-70.96754, 42.3229], [-70.95913, 42.32457], [-70.96573, 42.31347], [-70.9774, 42.31229]]], [[[-73.26496, 42.74594], [-73.14249, 42.74351], [-72.93026, 42.73916], [-72.80911, 42.73658], [-72.61635, 42.73123], [-72.45852, 42.72685], [-72.28595, 42.72163], [-72.12453, 42.71764], [-71.9814, 42.71329], [-71.92881, 42.71223], [-71.74582, 42.70729], [-71.56731, 42.70326], [-71.35187, 42.69815], [-71.33021, 42.69719], [-71.2942, 42.69699], [-71.27893, 42.71126], [-71.2679, 42.72589], [-71.2556, 42.73639], [-71.2455, 42.74259], [-71.2239, 42.74669], [-71.1818, 42.73759], [-71.1861, 42.79069], [-71.1656, 42.80869], [-71.1497, 42.81549], [-71.1325, 42.82139], [-71.0642, 42.80629], [-71.0536, 42.83309], [-71.0444, 42.84879], [-71.0312, 42.85909], [-70.9665, 42.86899], [-70.9308, 42.88459], [-70.9149, 42.88659], [-70.90277, 42.88653], [-70.88614, 42.88261], [-70.84862, 42.86094], [-70.83079, 42.86892], [-70.8173, 42.87229], [-70.81773, 42.85061], [-70.81269, 42.82287], [-70.80854, 42.81494], [-70.80522, 42.7818], [-70.79287, 42.74712], [-70.77227, 42.71106], [-70.77045, 42.70482], [-70.77579, 42.70067], [-70.77608, 42.69126], [-70.76442, 42.68565], [-70.75274, 42.68433], [-70.7446, 42.68131], [-70.72982, 42.6696], [-70.72783, 42.66593], [-70.70583, 42.65825], [-70.69123, 42.65579], [-70.68159, 42.66234], [-70.67364, 42.66995], [-70.66677, 42.67264], [-70.66355, 42.6776], [-70.6451, 42.68942], [-70.63774, 42.6892], [-70.63008, 42.6927], [-70.62325, 42.6869], [-70.62067, 42.6767], [-70.62279, 42.66087], [-70.60527, 42.65902], [-70.59547, 42.66034], [-70.5971, 42.65178], [-70.59174, 42.64851], [-70.59497, 42.6432], [-70.59147, 42.63982], [-70.59401, 42.63503], [-70.60561, 42.6349], [-70.61842, 42.62864], [-70.62048, 42.62303], [-70.62717, 42.62134], [-70.63222, 42.6168], [-70.63233, 42.60788], [-70.63563, 42.60024], [-70.64609, 42.59221], [-70.65473, 42.58223], [-70.66489, 42.58044], [-70.66604, 42.58408], [-70.657, 42.59825], [-70.65891, 42.6035], [-70.66556, 42.6091], [-70.67673, 42.60753], [-70.67649, 42.60333], [-70.68434, 42.59616], [-70.6808, 42.59346], [-70.68808, 42.58595], [-70.69293, 42.58421], [-70.69857, 42.57739], [-70.70819, 42.57558], [-70.71035, 42.57257], [-70.72969, 42.57151], [-70.74014, 42.57481], [-70.75728, 42.57046], [-70.76372, 42.56168], [-70.77748, 42.55936], [-70.79442, 42.5645], [-70.80409, 42.5616], [-70.81539, 42.5542], [-70.82329, 42.5515], [-70.83711, 42.55096], [-70.84548, 42.5482], [-70.85517, 42.54753], [-70.86089, 42.54465], [-70.86806, 42.54837], [-70.87519, 42.54434], [-70.88256, 42.53489], [-70.87892, 42.53214], [-70.86759, 42.53629], [-70.86421, 42.53343], [-70.86632, 42.52673], [-70.87757, 42.5235], [-70.88518, 42.51527], [-70.88637, 42.50861], [-70.87472, 42.50493], [-70.86402, 42.5186], [-70.85712, 42.52149], [-70.84562, 42.51748], [-70.84239, 42.50879], [-70.85166, 42.5002], [-70.84739, 42.49389], [-70.83381, 42.50587], [-70.83599, 42.4905], [-70.84159, 42.4876], [-70.84739, 42.4915], [-70.85779, 42.4903], [-70.87969, 42.4788], [-70.88649, 42.4702], [-70.88729, 42.4649], [-70.89429, 42.4609], [-70.90809, 42.4669], [-70.92199, 42.4667], [-70.92771, 42.46089], [-70.93499, 42.4579], [-70.93675, 42.44007], [-70.92891, 42.43831], [-70.92508, 42.4303], [-70.91319, 42.4277], [-70.90287, 42.42005], [-70.90569, 42.4162], [-70.9147, 42.41843], [-70.92843, 42.41708], [-70.93639, 42.4181], [-70.93699, 42.43042], [-70.94084, 42.43764], [-70.94103, 42.45234], [-70.94702, 42.45624], [-70.96047, 42.44617], [-70.96083, 42.44127], [-70.97551, 42.43158], [-70.98769, 42.4167], [-70.99059, 42.4071], [-70.98507, 42.40204], [-70.98034, 42.39151], [-70.96667, 42.38894], [-70.97251, 42.38504], [-70.97222, 42.37732], [-70.96603, 42.36634], [-70.96908, 42.36038], [-70.96314, 42.35582], [-70.95691, 42.3554], [-70.95329, 42.3497], [-70.96005, 42.34651], [-70.97526, 42.35898], [-70.98595, 42.35827], [-70.98955, 42.3545], [-70.99825, 42.35279], [-71.00688, 42.34704], [-71.01566, 42.33052], [-71.03278, 42.32841], [-71.04418, 42.32261], [-71.03325, 42.31699], [-71.04133, 42.30293], [-71.02422, 42.30152], [-71.01495, 42.30293], [-71.0178, 42.31312], [-71.00687, 42.32103], [-71.00235, 42.3191], [-71.00996, 42.31048], [-71.00758, 42.30293], [-71.00095, 42.30248], [-70.99047, 42.30802], [-70.98785, 42.30398], [-71.00425, 42.29923], [-71.00356, 42.29528], [-71.02065, 42.28658], [-71.01519, 42.27989], [-70.9961, 42.27122], [-70.99142, 42.26582], [-70.98263, 42.26565], [-70.97336, 42.26301], [-70.96735, 42.26817], [-70.94897, 42.2725], [-70.95125, 42.26107], [-70.95458, 42.25439], [-70.95268, 42.24876], [-70.94317, 42.2521], [-70.93723, 42.25773], [-70.92748, 42.25932], [-70.92483, 42.26334], [-70.92634, 42.26979], [-70.91706, 42.27254], [-70.90942, 42.26829], [-70.90752, 42.26231], [-70.89255, 42.26248], [-70.89421, 42.25509], [-70.88351, 42.2463], [-70.87781, 42.24929], [-70.87591, 42.25685], [-70.8828, 42.26811], [-70.8847, 42.27778], [-70.87828, 42.27831], [-70.88684, 42.29255], [-70.88732, 42.29765], [-70.90395, 42.30169], [-70.91037, 42.29906], [-70.92392, 42.30504], [-70.90756, 42.30789], [-70.89586, 42.30593], [-70.88946, 42.31048], [-70.88268, 42.31039], [-70.88124, 42.30066], [-70.87087, 42.28567], [-70.86181, 42.27597], [-70.85109, 42.26827], [-70.83107, 42.26742], [-70.81174, 42.26294], [-70.78872, 42.25392], [-70.7844, 42.24858], [-70.77631, 42.24895], [-70.77394, 42.25421], [-70.76634, 42.25474], [-70.76277, 42.25034], [-70.76476, 42.24406], [-70.76068, 42.24124], [-70.76016, 42.23504], [-70.74723, 42.22182], [-70.73914, 42.21962], [-70.73056, 42.21094], [-70.71299, 42.20443], [-70.71871, 42.18485], [-70.71476, 42.17658], [-70.7143, 42.16878], [-70.70626, 42.16314], [-70.68531, 42.13303], [-70.66393, 42.10834], [-70.64017, 42.08863], [-70.63848, 42.08158], [-70.64735, 42.07633], [-70.64819, 42.06844], [-70.64321, 42.05082], [-70.63086, 42.03605], [-70.62028, 42.02709], [-70.61098, 42.01574], [-70.59789, 42.00455], [-70.6027, 42.00214], [-70.61405, 42.00661], [-70.62254, 42.00214], [-70.63192, 41.99286], [-70.63914, 41.99389], [-70.6412, 42.00593], [-70.63965, 42.0108], [-70.62986, 42.00146], [-70.61422, 42.01115], [-70.61779, 42.01751], [-70.64434, 42.0459], [-70.65087, 42.04625], [-70.65605, 42.04205], [-70.66437, 42.04116], [-70.66936, 42.03712], [-70.67167, 42.02139], [-70.66751, 42.01232], [-70.67093, 42.00779], [-70.6788, 42.00551], [-70.6868, 42.01276], [-70.69581, 42.01335], [-70.7122, 42.00759], [-70.71003, 41.99954], [-70.70002, 41.99826], [-70.69898, 41.9871], [-70.69099, 41.9813], [-70.6822, 41.97988], [-70.67626, 41.97229], [-70.6532, 41.95249], [-70.64678, 41.94931], [-70.63276, 41.9486], [-70.64869, 41.97229], [-70.65463, 41.97794], [-70.65083, 41.98218], [-70.64417, 41.97458], [-70.63157, 41.95302], [-70.62351, 41.94327], [-70.61649, 41.9402], [-70.60817, 41.9407], [-70.59808, 41.94777], [-70.58357, 41.95001], [-70.56777, 41.9395], [-70.56597, 41.93623], [-70.54397, 41.92628], [-70.53787, 41.92095], [-70.54639, 41.91675], [-70.54595, 41.90716], [-70.53208, 41.88957], [-70.53049, 41.86549], [-70.52557, 41.85873], [-70.53255, 41.84066], [-70.53626, 41.83466], [-70.54206, 41.83126], [-70.54317, 41.82445], [-70.54103, 41.81575], [-70.53266, 41.8048], [-70.51741, 41.79095], [-70.49452, 41.77824], [-70.49405, 41.77388], [-70.47155, 41.76156], [-70.41248, 41.7444], [-70.37534, 41.73878], [-70.29096, 41.73431], [-70.27428, 41.72341], [-70.26365, 41.71412], [-70.2592, 41.71395], [-70.24952, 41.72097], [-70.23932, 41.72563], [-70.23465, 41.73204], [-70.21607, 41.74298], [-70.18925, 41.75198], [-70.1838, 41.75058], [-70.14991, 41.75698], [-70.14153, 41.76007], [-70.12198, 41.75884], [-70.09606, 41.76655], [-70.08299, 41.76896], [-70.07246, 41.77294], [-70.06431, 41.77284], [-70.02473, 41.78736], [-70.00846, 41.80079], [-70.00384, 41.80852], [-70.00449, 41.83883], [-70.00901, 41.87662], [-70.00019, 41.88694], [-70.00292, 41.89032], [-70.0185, 41.89153], [-70.02424, 41.89634], [-70.02121, 41.90015], [-70.01361, 41.90121], [-70.01337, 41.90599], [-70.02555, 41.9117], [-70.0323, 41.92044], [-70.02739, 41.92933], [-70.04499, 41.93005], [-70.05496, 41.92792], [-70.06162, 41.9235], [-70.05895, 41.91711], [-70.06567, 41.91166], [-70.06572, 41.89964], [-70.07304, 41.89978], [-70.07401, 41.93865], [-70.07722, 41.94336], [-70.07742, 41.9855], [-70.08377, 42.01204], [-70.08958, 42.0249], [-70.09559, 42.03283], [-70.10806, 42.0436], [-70.12304, 42.05167], [-70.14861, 42.06093], [-70.15541, 42.06241], [-70.16978, 42.05974], [-70.17847, 42.05642], [-70.18682, 42.05045], [-70.19497, 42.0364], [-70.20874, 42.03075], [-70.2187, 42.04585], [-70.22862, 42.05393], [-70.24538, 42.06373], [-70.23809, 42.07288], [-70.22563, 42.0786], [-70.2069, 42.0819], [-70.1893, 42.08234], [-70.16017, 42.07863], [-70.11597, 42.06764], [-70.08262, 42.05466], [-70.05853, 42.04036], [-70.0335, 42.01774], [-70.0119, 41.98972], [-69.98608, 41.9496], [-69.9686, 41.9117], [-69.94531, 41.84522], [-69.94135, 41.82279], [-69.93802, 41.80951], [-69.92865, 41.74125], [-69.92839, 41.70845], [-69.93042, 41.69194], [-69.93375, 41.67863], [-69.94373, 41.66478], [-69.94397, 41.65555], [-69.94753, 41.65146], [-69.9568, 41.6298], [-69.95777, 41.62036], [-69.96719, 41.61196], [-69.97605, 41.61167], [-69.98318, 41.6083], [-69.98841, 41.59443], [-69.98936, 41.58146], [-69.98821, 41.5547], [-69.99198, 41.54749], [-69.99768, 41.54233], [-70.00386, 41.54055], [-70.01123, 41.54393], [-70.01361, 41.55105], [-70.00861, 41.55798], [-69.99885, 41.5659], [-69.99388, 41.5763], [-69.99131, 41.58872], [-69.99221, 41.60332], [-69.98521, 41.61312], [-69.98556, 41.61967], [-69.97748, 41.63079], [-69.97592, 41.63886], [-69.97049, 41.64546], [-69.97572, 41.65374], [-69.98532, 41.65821], [-69.99636, 41.66718], [-70.00701, 41.67158], [-70.01421, 41.67197], [-70.02935, 41.66774], [-70.04051, 41.6674], [-70.06211, 41.66445], [-70.0657, 41.66236], [-70.07597, 41.66395], [-70.08924, 41.66281], [-70.11651, 41.6555], [-70.14088, 41.65042], [-70.16834, 41.652], [-70.19519, 41.64791], [-70.198, 41.64415], [-70.20708, 41.6425], [-70.21977, 41.63647], [-70.24587, 41.62848], [-70.25621, 41.6207], [-70.2596, 41.61086], [-70.26759, 41.61091], [-70.26969, 41.61777], [-70.26913, 41.62574], [-70.27452, 41.63293], [-70.29062, 41.6352], [-70.30025, 41.63246], [-70.30065, 41.62951], [-70.31663, 41.62545], [-70.32159, 41.63051], [-70.33807, 41.63634], [-70.35163, 41.63469], [-70.36035, 41.63107], [-70.36985, 41.61589], [-70.37915, 41.61136], [-70.40058, 41.60638], [-70.40853, 41.60734], [-70.42681, 41.60472], [-70.43725, 41.60533], [-70.44262, 41.59905], [-70.44529, 41.59181], [-70.46128, 41.57182], [-70.47626, 41.5585], [-70.49324, 41.55204], [-70.52233, 41.54896], [-70.52862, 41.54672], [-70.53882, 41.55126], [-70.54682, 41.55141], [-70.55969, 41.54833], [-70.57377, 41.54687], [-70.58055, 41.54424], [-70.59381, 41.5451], [-70.60184, 41.54208], [-70.61108, 41.54299], [-70.63361, 41.53825], [-70.64363, 41.53236], [-70.65662, 41.51478], [-70.66829, 41.51795], [-70.67305, 41.52365], [-70.68541, 41.52134], [-70.68698, 41.52949], [-70.68327, 41.5329], [-70.67638, 41.52899], [-70.66806, 41.5329], [-70.66651, 41.53996], [-70.65866, 41.54339], [-70.6543, 41.54993], [-70.6539, 41.56516], [-70.64275, 41.57238], [-70.64204, 41.58307], [-70.65245, 41.60521], [-70.65199, 41.61018], [-70.64685, 41.6135], [-70.64613, 41.61972], [-70.64, 41.62462], [-70.64525, 41.63355], [-70.65327, 41.63898], [-70.65072, 41.64613], [-70.63074, 41.65022], [-70.6248, 41.65573], [-70.62741, 41.66088], [-70.63502, 41.66319], [-70.64072, 41.65946], [-70.65196, 41.66304], [-70.65375, 41.66709], [-70.64191, 41.67153], [-70.63288, 41.67029], [-70.63359, 41.67632], [-70.64595, 41.68094], [-70.66204, 41.68094], [-70.64596, 41.69379], [-70.62544, 41.69869], [-70.62365, 41.7074], [-70.62653, 41.713], [-70.63972, 41.71736], [-70.6488, 41.71803], [-70.65047, 41.71342], [-70.66045, 41.70508], [-70.67406, 41.69137], [-70.67614, 41.69265], [-70.65621, 41.71339], [-70.664, 41.7162], [-70.67923, 41.72743], [-70.68826, 41.7237], [-70.69705, 41.7292], [-70.70617, 41.72898], [-70.71874, 41.73574], [-70.72633, 41.73273], [-70.72082, 41.72761], [-70.72095, 41.72322], [-70.72853, 41.72287], [-70.7213, 41.71297], [-70.71203, 41.70703], [-70.71423, 41.70173], [-70.72748, 41.70241], [-70.71835, 41.69016], [-70.71504, 41.68101], [-70.72153, 41.68147], [-70.72939, 41.68814], [-70.7396, 41.69177], [-70.74435, 41.69798], [-70.75535, 41.69433], [-70.74911, 41.68041], [-70.75838, 41.68058], [-70.76384, 41.67686], [-70.75671, 41.66691], [-70.75706, 41.65289], [-70.76242, 41.65271], [-70.76932, 41.64115], [-70.77671, 41.65076], [-70.79083, 41.65323], [-70.79522, 41.65093], [-70.809, 41.65839], [-70.8216, 41.65484], [-70.82326, 41.64898], [-70.80466, 41.64116], [-70.80021, 41.63175], [-70.81028, 41.62487], [-70.81768, 41.62343], [-70.82207, 41.62749], [-70.8353, 41.62453], [-70.84416, 41.62898], [-70.85965, 41.62412], [-70.85513, 41.62183], [-70.85366, 41.61397], [-70.84964, 41.61025], [-70.84798, 41.60296], [-70.84323, 41.59657], [-70.85018, 41.59353], [-70.85672, 41.58371], [-70.86024, 41.59463], [-70.86366, 41.59759], [-70.86295, 41.60385], [-70.8689, 41.61466], [-70.86836, 41.62266], [-70.87266, 41.62782], [-70.88921, 41.6329], [-70.89457, 41.62411], [-70.90883, 41.62358], [-70.9132, 41.61927], [-70.90452, 41.61036], [-70.89861, 41.59265], [-70.91081, 41.59551], [-70.91658, 41.60748], [-70.92237, 41.61434], [-70.93046, 41.61327], [-70.93117, 41.60687], [-70.92739, 41.59406], [-70.93372, 41.58029], [-70.94159, 41.58103], [-70.9488, 41.57904], [-70.9473, 41.57366], [-70.93783, 41.56524], [-70.93456, 41.54875], [-70.92852, 41.53978], [-70.94178, 41.54012], [-70.9463, 41.53756], [-70.94793, 41.5298], [-70.95488, 41.52757], [-70.95262, 41.51812], [-70.9566, 41.51546], [-70.96135, 41.5297], [-70.96658, 41.53166], [-70.98013, 41.52756], [-70.98465, 41.52044], [-70.98156, 41.51368], [-70.98396, 41.5089], [-71.00327, 41.51191], [-71.01935, 41.50886], [-71.02234, 41.50435], [-71.04101, 41.49753], [-71.04859, 41.50266], [-71.07069, 41.50888], [-71.08566, 41.50929], [-71.09305, 41.50421], [-71.10681, 41.50247], [-71.12057, 41.49745], [-71.1224, 41.52216], [-71.13131, 41.59231], [-71.14059, 41.6051], [-71.14047, 41.62389], [-71.13569, 41.6284], [-71.13289, 41.6601], [-71.17609, 41.6681], [-71.17599, 41.6714], [-71.19564, 41.67509], [-71.2248, 41.7105], [-71.26139, 41.7523], [-71.3279, 41.7805], [-71.3339, 41.7945], [-71.3408, 41.8002], [-71.3392, 41.809], [-71.3472, 41.8231], [-71.3449, 41.828], [-71.3352, 41.8355], [-71.3422, 41.8448], [-71.334, 41.8623], [-71.3408, 41.8816], [-71.3387, 41.8984], [-71.3817, 41.8932], [-71.3814, 42.0188], [-71.4999, 42.0172], [-71.52761, 42.015], [-71.57691, 42.0141], [-71.76601, 42.00974], [-71.79924, 42.00806], [-71.80065, 42.02357], [-71.89078, 42.02437], [-71.98733, 42.02688], [-72.0635, 42.02735], [-72.13569, 42.03025], [-72.24952, 42.03163], [-72.31715, 42.03191], [-72.45668, 42.034], [-72.52813, 42.0343], [-72.57323, 42.03014], [-72.58233, 42.0247], [-72.60693, 42.025], [-72.60793, 42.0308], [-72.64313, 42.0324], [-72.69593, 42.03679], [-72.75584, 42.0362], [-72.75174, 42.0302], [-72.76614, 42.0077], [-72.76674, 42.003], [-72.81674, 41.9976], [-72.81354, 42.03649], [-72.84714, 42.03689], [-72.86362, 42.03771], [-72.99955, 42.03865], [-73.05325, 42.03986], [-73.2298, 42.04488], [-73.29442, 42.04698], [-73.43281, 42.05059], [-73.48731, 42.04964], [-73.49688, 42.04968], [-73.50814, 42.08626], [-73.47592, 42.174], [-73.44289, 42.26394], [-73.38209, 42.42949], [-73.35253, 42.51], [-73.307, 42.63265], [-73.26496, 42.74594]]]],
        },
        "properties": {
          "geoid2": 25,
          "population": 6933045.34440539
        }
      }
    ]
  }
  ```


## [2.6.4] - 2019-02-20
### Changes
- Changes the VBA docs to give a more detailed account of how to use and update queries

## [2.6.3] - 2019-02-12
### Fixes
- Fixes `APIQueryParams.pretty_print_vba` for mile radius and drivetime filters

## [2.6.2] - 2019-02-01
### Fixes
- Fixes a bug caused by users running the code without a debug token. The debug token has been removed and the code will rely on the actual API token

## [2.6.1] - 2019-01-28
### Fixes
- Fixes reference to image names in docs

## [2.6.0] - 2019-01-28
### Adds
- Adds examples to the docs showing how to use Blaise ML to generate API queries for each supported language

## [2.5.6] - 2019-01-26
### Adds
- Adds `MileRadiusFilter` and `DrivetimeFilter` to `strato_query`
- Updates `submit_api_query` to return `data.frame` with correct `numeric` types in R

## [2.5.5] - 2019-01-25
### Fixes
- Adds spacing for comma-separated arguments

## [2.5.4] - 2019-01-25
### Fixes
- Bug fixes in `pretty_print_r` and `pretty_print_vba` for `query_type`

## [2.5.3] - 2019-01-25
### Fixes
- Fixes argument name in `pretty_print` method

## [2.5.2] - 2019-01-25
### Adds
- Adds a pretty print method that can be called on the `APIQueryParams` class, and any class inheriting from the same.
It will return a string that mirrors R code, and can be copied and pasted directly into an R script.

## [2.5.1] - 2019-01-25
### Adds
- Adds a pretty print method that can be called on the `APIQueryParams` class, and any class inheriting from the same.
It will return a string that mirrors Excel VBA code, and can be copied and pasted directly into a VBA script.

## [2.5.0] - 2019-01-25
### Adds
- Adds a pretty print method that can be called on the `APIQueryParams` class, and any class inheriting from the same.
It will return a string that mirrors the Python code, and can be copied and pasted directly into a Python script.
- Adds default values for the `query_type`, allowing this value to be omitted when creating instances of the `APIQueryParams` classes

## [2.4.0] - 2019-01-09
### Adds
- Adds example queries to demonstrate different ways of using `strato-query`

## [2.3.1] - 2019-01-06
### Changes
- `BaseAPIQuery.submit_query` now includes optional `headers` argument to send with request

## [2.3.0] - 2019-01-03
### Adds
- Adds new filters to `__all__` declaration
- Adds new classes, `APIMeanQueryParams` and `APIMedianQueryParams`, which require the values necessary for the related queries
- Adds new tests for the new query types

## [2.2.0] - 2019-01-02
### Adds
- Adds new filters for "not in" and "not equal"

## [2.1.2] - 2018-12-27
### Adds
- Adds optional `median_variable_name` parameter to `APIQueryParams` to allow for median queries

## [2.1.1] - 2018-12-27
### Adds
- Adds optional `order` parameter to `APIQueryParams` to allow for sorting results

## [2.1.0] - 2018-12-27
### Changes
- Changes the `InFilter` so it will raise an error if it receives an empty list or `None` as the `val`.

## [2.0.0] - 2018-12-26
### Changes
- **Breaking change**. Combines the query param classes into one while allowing for unlimited nesting of joins.

Example use:

```python
from strato_query.base_API_query import *
from strato_query.standard_filters import *

class ExampleAPIJoinQuery(BaseAPIQuery):
    @classmethod
    def get_df_from_API_call(cls, **kwargs):
        df = cls.query_api_df(
            query_params=APIQueryParams(
                table='table_1',
                data_fields=('a', 'b', 'c'),
                data_filters=(),
                query_type='COUNT',
                aggregations=(),
                groupby=(),
                join=APIQueryParams(
                    table='table_2',
                    data_fields=('c', 'd'),
                    data_filters=(),
                    query_type='COUNT',
                    aggregations=(),
                    groupby=(),
                    on=dict(left=('c',), right=('c',)),
                    join=APIQueryParams(
                        table='table_3',
                        data_fields=('d',),
                        data_filters=(),
                        query_type='COUNT',
                        aggregations=(),
                        groupby=(),
                        on=dict(left=('d',), right=('d',)),
                    )
                )
            )
        )

        return df
```

## [1.0.0] - 2018-12-26
### v1 release
- Version 1.0.0 release
