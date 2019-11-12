"""
StratoDem Analytics : constants
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

December 26, 2018
"""

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
