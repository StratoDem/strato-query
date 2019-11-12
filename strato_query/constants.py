"""
StratoDem Analytics : constants
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

December 26, 2018
"""

from types import MappingProxyType

API_URL = 'https://api.stratodem.com/api'

MAX_RETRIES = 3

SPECIAL_FILTER_SET = frozenset({
    'mile_radius',
    'mile_radius_simple',
    'mile_radius_unweighted',
    'drivetime',
    'drivetime_simple',
    'drivetime_unweighted',
    'drivetime_destination',
    'drivetime_destination_simple',
    'drivetime_destination_unweighted',
    'walktime',
    'walktime_unweighted',
    'walktime_destination',
    'walktime_destination_unweighted',
    'intersects',
    'intersects_weighted',
})

MAP_SPECIAL_FILTER_TO_FUNC = MappingProxyType({
    'mile_radius': 'mile_radius_filter',
    'mile_radius_simple': 'mile_radius_filter',
    'mile_radius_unweighted': 'mile_radius_filter',
    'drivetime': 'drivetime_filter',
    'drivetime_simple': 'drivetime_filter',
    'drivetime_unweighted': 'drivetime_filter',
    'drivetime_destination': 'drivetime_filter',
    'drivetime_destination_simple': 'drivetime_filter',
    'drivetime_destination_unweighted': 'drivetime_filter',
    'walktime': 'walktime_filter',
    'walktime_unweighted': 'walktime_filter',
    'walktime_destination': 'walktime_filter',
    'walktime_destination_unweighted': 'walktime_filter',
    'intersects': 'intersects_filter',
    'intersects_weighted': 'intersects_filter',
})
