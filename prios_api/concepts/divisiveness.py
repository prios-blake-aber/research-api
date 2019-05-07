"""
Divisiveness: Statistic of disagreement between a set of opinions.
"""

from typing import List, TypeVar
from prios_api.src import foundation
from prios_api.domain_objects import objects

StringOrFloat = TypeVar("StringOrFloat", str, float)
_THRESHOLD_HIGH = 1.7
_THRESHOLD_STD_SCALE = 1.0
_THRESHOLD_STD_MAPPED_SCALE = 0.5
_THRESHOLD_POLES = 0.25
_MINIMUM_THRESH = 0.7



def divisiveness_stat(values: List[float], value_type: objects.QuestionType,
                      map_to_sentiment: bool = True) -> float:
    """
    Divisiveness is the standard deviation of opinions.

    Parameters
    ----------
    values
        Numerical values whose divisiveness is being calculated.
    value_type
        Type of value
    map_to_sentiment
        Map values to positive, neutral, or negative sentiment prior to taking standard
        deviation. Default is True.

    Returns
    -------
    float
        Divisiveness measure.
    """
    if map_to_sentiment:
        mapped_values = [foundation.map_values(vi, value_type) for vi in values]
        return foundation.standard_deviation(mapped_values)
    else:
        return foundation.standard_deviation(values)


