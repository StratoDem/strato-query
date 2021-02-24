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
})

MILE_BUFFER_TYPES = frozenset({
    'mile_radius',
    'mile_radius_simple',
    'mile_radius_unweighted',
})

MAP_SPECIAL_FILTER_TO_R_FUNC = MappingProxyType({
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
})

MAP_SPECIAL_FILTER_TO_VBA_FUNC = MappingProxyType({
    'mile_radius': 'mileRadiusFilter',
    'mile_radius_simple': 'mileRadiusFilter',
    'mile_radius_unweighted': 'mileRadiusFilter',
    'drivetime': 'drivetimeFilter',
    'drivetime_simple': 'drivetimeFilter',
    'drivetime_unweighted': 'drivetimeFilter',
    'drivetime_destination': 'drivetimeFilter',
    'drivetime_destination_simple': 'drivetimeFilter',
    'drivetime_destination_unweighted': 'drivetimeFilter',
    'walktime': 'walktimeFilter',
    'walktime_unweighted': 'walktimeFilter',
    'walktime_destination': 'walktimeFilter',
    'walktime_destination_unweighted': 'walktimeFilter',
})

BUFFERS_TUPLE = (
    'half-mile',
    'one-mile',
    'two-mile',
    'three-mile',
    'four-mile',
    'five-mile',
    'six-mile',
    'seven-mile',
    'eight-mile',
    'nine-mile',
    'ten-mile',
    'eleven-mile',
    'twelve-mile',
    'thirteen-mile',
    'fourteen-mile',
    'fifteen-mile',
    'sixteen-mile',
    'seventeen-mile',
    'eighteen-mile',
    'nineteen-mile',
    'twenty-mile',
    'twenty-five-mile',
    'thirty-mile',
    'fifty-mile',
    'sixty-mile',
    'five-min',
    'ten-min',
    'fifteen-min',
    'twenty-min',
    'thirty-min',
    'forty-five-min',
    'sixty-min',
    'five-traffic',
    'ten-traffic',
    'fifteen-traffic',
    'twenty-traffic',
    'thirty-traffic',
    'forty-five-traffic',
    'sixty-traffic',
    'ten-walk',
    'fifteen-walk',
    'twenty-walk',
    'thirty-walk',
    'five-min-destination',
    'ten-min-destination',
    'fifteen-min-destination',
    'twenty-min-destination',
    'thirty-min-destination',
    'forty-five-min-destination',
    'sixty-min-destination',
    'five-traffic-destination',
    'ten-traffic-destination',
    'fifteen-traffic-destination',
    'twenty-traffic-destination',
    'thirty-traffic-destination',
    'forty-five-traffic-destination',
    'sixty-traffic-destination',
    'ten-walk-destination',
    'fifteen-walk-destination',
    'twenty-walk-destination',
    'thirty-walk-destination',
)
