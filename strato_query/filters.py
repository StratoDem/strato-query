"""
StratoDem Analytics : filters
Principal Author(s) : Eric Linden, Michael Clawar
Secondary Author(s) :
Description :

Notes :

August 21, 2019
"""

import abc
from typing import List, Union, Optional


__all__ = [
    'BaseFilter',
    'BetweenFilter',
    'EqualToFilter',
    'InFilter',
    'GreaterThanFilter',
    'LessThanFilter',
    'GreaterThanOrEqualToFilter',
    'LessThanOrEqualToFilter',
    'NotEqualToFilter',
    'NotInFilter',
    'DrivetimeFilter',
    'MileRadiusFilter',
    'IntersectsFilter',
    'OverlapsFilter',
]


class BaseFilter(abc.ABC):
    def __init__(self, filter_type: str, filter_value, filter_variable: str):
        self._filter_type = filter_type
        self._filter_value = filter_value
        self._filter_variable = filter_variable

    def to_dict(self) -> dict:
        return dict(
            filter_type=self._filter_type,
            filter_value=self._filter_value,
            filter_variable=self._filter_variable)


class EqualToFilter(BaseFilter):
    """Construct a filter that generates var = val comparisons"""
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='eq',
                         filter_value=val,
                         filter_variable=var)


class BetweenFilter(BaseFilter):
    def __init__(self, var: str, val: List[Union[float, int]]):
        super().__init__(filter_type='between',
                         filter_value=val,
                         filter_variable=var)


class InFilter(BaseFilter):
    def __init__(self, var: str, val: List[Union[float, int, str]]):
        if val is None or len(val) < 1:
            raise ValueError('InFilter does not accept an empty list, nor a None value. \n'
                             'var: {}, val: {}'.format(var, val))
        super().__init__(filter_type='in',
                         filter_value=val,
                         filter_variable=var)


class GreaterThanFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='gt',
                         filter_value=val,
                         filter_variable=var)


class LessThanFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='lt',
                         filter_value=val,
                         filter_variable=var)


class GreaterThanOrEqualToFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='ge',
                         filter_value=val,
                         filter_variable=var)


class LessThanOrEqualToFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='le',
                         filter_value=val,
                         filter_variable=var)


class NotEqualToFilter(BaseFilter):
    def __init__(self, var: str, val: Union[float, int, str]):
        super().__init__(filter_type='ne',
                         filter_value=val,
                         filter_variable=var)


class NotInFilter(BaseFilter):
    def __init__(self, var: str, val: List[Union[float, int, str]]):
        if val is None or len(val) < 1:
            raise ValueError('NotInFilter does not accept an empty list, nor a None value. \n'
                             'var: {}, val: {}'.format(var, val))
        super().__init__(filter_type='nin',
                         filter_value=val,
                         filter_variable=var)


class MileRadiusFilter(BaseFilter):
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 miles: Union[int, float],
                 detailed_type: str = 'mile_radius'):
        """
        Filter a query to geographies contained by the drive time area

        Parameters
        ----------
        latitude: float
            Center latitude
        longitude: float
            Center longitude
        miles: int or float
            Miles from latitude-longitude center
        detailed_type: str
            One of:
            - 'mile_radius': use a normal mile radius, which weights results
            - 'mile_radius_simple': use a mile radius with weights, but using simplified shapes
            - 'mile_radius_unweighted': return unweighted results (used to get all geographies
                intersecting at all with the mile radius buffer)
        """
        assert detailed_type in {'mile_radius', 'mile_radius_simple', 'mile_radius_unweighted'}

        super().__init__(
            filter_type=detailed_type,
            filter_variable='',
            filter_value=dict(latitude=latitude, longitude=longitude, miles=miles))


class DrivetimeFilter(BaseFilter):
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 minutes: Union[int, float],
                 detailed_type: str = 'drivetime',
                 with_traffic: bool = False,
                 start_time: Optional[str] = None):
        """
        Filter a query to geographies contained by the drive time area

        Parameters
        ----------
        latitude: float
            Center latitude
        longitude: float
            Center longitude
        minutes: int or float
            Minutes drive from latitude-longitude center
        detailed_type: str
            One of:
            - 'drivetime': use a normal drivetime, which weights results
            - 'drivetime_simple': use a drivetime with weights, but using simplified shapes
            - 'drivetime_unweighted': return unweighted results (used to get all geographies
                intersecting at all with the drive time area)
        with_traffic: bool
            Use traffic estimates to compute the drive time area?
        start_time: str
            The departure time for the drivetime, used in concert with "with_traffic" set to True
            e.g., "2019-05-25T18:00:00"
        """
        assert detailed_type in {'drivetime', 'drivetime_simple', 'drivetime_unweighted'}
        assert isinstance(with_traffic, bool)
        assert start_time is None or isinstance(start_time, str)

        super().__init__(
            filter_type=detailed_type,
            filter_variable='',
            filter_value=dict(
                latitude=latitude,
                longitude=longitude,
                minutes=minutes,
                traffic='enabled' if with_traffic else 'disabled',
                start_time=start_time))


class IntersectsFilter(BaseFilter):
    def __init__(self, var: str, val: dict):
        super().__init__(
            filter_type='intersects',
            filter_variable=var,
            filter_value=val)


class OverlapsFilter(BaseFilter):
    def __init__(self,
                 var: str,
                 geometry: str,
                 miles: Optional[Union[int, float]] = 0):
        """
        Filter a query by geometries overlapping the market shape and surrounding buffer

        Parameters
        ----------
        var: str
            The name of the geometry column against which this filter will check
        geometry: str
            The geojson for the market shape. Can be a single point, or a polygon

            Examples
                geometry='{"type": "Point", "coordinates": [-96.91386923077042, 33.08536026887235]}'
                geometry='{"type": "Polygon",
                           "coordinates": [[[-71.06944084167479, 42.35721199960259],
                                            [-71.07012748718262, 42.34205151655285],
                                            [-71.03416442871094, 42.342685919682445],
                                            [-71.03579521179199, 42.35537263800411],
                                            [-71.05021476745605, 42.3647591610627],
                                            [-71.06944084167479, 42.35721199960259]]]}'


        miles: Optional[Union[int, float]]
            Default 0. The number of miles out from the given market geometry. If that geometry
            is a point, this value should be set explicitly. If the geometry is a polygon, this
            value can be omitted.
        """
        assert isinstance(var, str)
        assert isinstance(geometry, str)
        assert miles is None or isinstance(miles, (int, float))

        super().__init__(
            filter_type='overlaps',
            filter_variable=var,
            filter_value=dict(
                geometry=geometry,
                miles=miles))
