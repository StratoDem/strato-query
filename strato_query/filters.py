"""
StratoDem Analytics : filters
Principal Author(s) : Eric Linden, Michael Clawar
Secondary Author(s) :
Description :

Notes :

August 21, 2019
"""

import abc
from typing import List, Union


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
    def __init__(self, latitude: float, longitude: float, miles: Union[int, float]):
        super().__init__(
            filter_type='mile_radius',
            filter_variable='',
            filter_value=dict(latitude=latitude, longitude=longitude, miles=miles))


class DrivetimeFilter(BaseFilter):
    def __init__(self, latitude: float, longitude: float, minutes: Union[int, float]):
        super().__init__(
            filter_type='drivetime',
            filter_variable='',
            filter_value=dict(latitude=latitude, longitude=longitude, minutes=minutes))


class IntersectsFilter(BaseFilter):
    def __init__(self, var: str, val: dict):
        super().__init__(
            filter_type='intersects',
            filter_variable=var,
            filter_value=val)
