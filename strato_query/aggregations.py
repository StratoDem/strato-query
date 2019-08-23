"""
StratoDem Analytics : aggregations
Principal Author(s) : Michael Clawar
Secondary Author(s) :
Description :

Notes :

August 23, 2019
"""

__all__ = [
    'SumAggregation',
]


class BaseAggregation:
    def to_dict(self) -> dict:
        raise NotImplementedError


class SumAggregation(BaseAggregation):
    def __init__(self, var: str):
        self._var = var

    def to_dict(self) -> dict:
        return {'aggregation_func': 'sum', 'variable_name': self._var}
