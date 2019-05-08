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


def divisiveness_stat(ar: List[StringOrFloat], value_type: objects.QuestionType) -> float:
    """
    Divisiveness.

    TODO: How are N/A's being represented? We shouldn't assume they're being filtered.

    Parameters
    ----------
    ar
    value_type

    Returns
    -------
    float
        Divisiveness value

    Examples
    --------
    >>> divisiveness_stat([1], value_type = objects.QuestionType.SCALE)
    nan
    >>> round(divisiveness_stat([1,10], value_type = objects.QuestionType.SCALE), 3)
    1.414
    >>> round(divisiveness_stat([1, 3, 4, 5, 5], value_type = objects.QuestionType.LIKERT), 3)
    0.894
    >>> round(divisiveness_stat(['Give up', 'Push Ahead and see what happens', 'Delay',
    ... 'Do whatever it takes to make it work'], value_type = objects.QuestionType.CATEGORICAL), 2)
    0.5
    >>> round(divisiveness_stat(["Yes", "No", "Yes", "No"], value_type = objects.QuestionType.BINARY), 2)
    0.58
    """
    if value_type in [objects.QuestionType.SCALE, objects.QuestionType.LIKERT, objects.QuestionType.BINARY]:
        mapped_values = foundation.map_values(ar, value_type)
        return foundation.standard_deviation(mapped_values)
    else:
        count = [v for k, v in foundation.counts(ar).items()]
        max_count = max(count)
        mapped_ar = [0]*max_count + [1]*(len(ar) - max_count)
        return foundation.standard_deviation(mapped_ar)

