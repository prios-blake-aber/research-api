
"""
TBD
"""

from typing import List, Callable, Optional, TypeVar, Dict, Tuple
from collections import Counter
import numpy as np
from scipy.stats import zscore
from prios_api.domain_objects import objects
import itertools

StringOrFloat = TypeVar("StringOrFloat", str, float)


def map_values(values: List[float], value_type: objects.QuestionType):
    """
    Maps values from one numeric range to a different numeric range. Currently, mapping is to
    defined for 1-to-10 or 1-to-5 ranges to "Semantic Buckets" (Positive, Negative, or Neutral).

    TODO: Add parameter for mapping lambda and to_type.
    TODO: Hard-coded to map 1-to-10 or 1-to-5 values to "Semantic Buckets".

    Parameters
    ----------
    values
        Input data
    value_type
        Type of

    Returns
    -------
    List[float]
        Numeric values on different scale. Currently hard-coded to legacy semantic bucket scale.
    """

    # TODO: Finalize value-type object.
    if value_type == objects.NumericRange.ONE_TO_TEN:
        value_type = objects.QuestionType.SCALE
    if value_type == objects.NumericRange.ONE_TO_FIVE:
        value_type = objects.QuestionType.LIKERT

    if value_type == objects.QuestionType.SCALE:
        (low_thresh, high_thresh) = (5, 7)
    elif value_type == objects.QuestionType:
        (low_thresh, high_thresh) = (2.5, 3.5)
    else:
        return values

    return np.digitize(values, [low_thresh, high_thresh])


def standard_deviation(x: List[float]) -> float:
    return np.nanstd(np.array(x), ddof=1)


def weighted_average(values: List[float], **kwargs) -> float:
    """
    Average of numeric values.

    Parameters
    ----------
    values
    kwargs

    Returns
    -------
    float
    """
    return np.average(values, **kwargs)


def percent_satisfying_condition(ar: List[float], condition: Callable) -> Optional[float]:
    """
    Percent of values in an array that satisfy condition.

    Parameters
    ----------
    ar
        List of numeric values
    condition
        Calculates percent of values that satisfy this condition.

    Returns
    -------
    Percentage (between 0 and 1, inclusive) if `x` has 1 or more elements. Otherwise it returns
    None.

    Examples
    --------
    >>> greater_than_two = lambda x: x > 2
    >>> percent_satisfying_condition([1, 2, 3, 4], greater_than_two)
    0.5
    >>> greater_than_four = lambda x: x > 4
    >>> percent_satisfying_condition([1, 2, 3, 4], greater_than_four)
    0.0
    >>> percent_satisfying_condition([], greater_than_four)
    """
    if len(ar) > 0:
        subset = [x for x in ar if condition(x)]
        return len(subset) / len(ar)
    else:
        return None


def counts(ar: List[StringOrFloat], normalize: bool = False) -> Dict[StringOrFloat, float]:
    """
    Gets proportions of each
    Parameters
    ----------
    ar
    normalize


    Returns
    -------
    Dict[StringOrFloat, float]

    Examples
    --------
    >>> counts([])
    {}
    >>> counts(['a', 'a', 'a','b'])
    {'a': 0.75, 'b': 0.25}
    >>> counts([1, 1, 1, 2])
    {1: 0.75, 2: 0.25}
    >>> counts([1, 1, 1, 2])
    {1: 0.75, 2: 0.25}
    """
    if len(ar) == 0:
        return dict()
    c = Counter(ar)

    if normalize:
        return {i: c[i] / len(ar) for i in c}
    else:
        return {i: c[i] for i in c}


def percent_of_total(values_and_weights: List[Tuple[StringOrFloat, float]]) -> Dict[StringOrFloat, float]:
    """
    Percent of total.

    Parameters
    ----------
    values_and_weights

    Returns
    -------
    Dict[StringOrFloat, float]
    """
    total = sum([x[1] for x in values_and_weights])
    sorted_responses = sorted(values_and_weights, key=lambda x: x[0])
    result = dict()
    for choice, weight in itertools.groupby(sorted_responses, key=lambda x: x[0]):
        result[choice] = sum(list(weight)) / total
    return result


def addition(values : List[float]):
    return sum(values)


def map_to_z_score(values: List[float]) -> List[float]:
    """
    Z-score: Subtract values by their mean and divide by standard deviation.

    Parameters
    ----------
    values

    Returns
    -------
    List[float]
        Z-scores

    Examples
    --------
    >>> map_to_z_score([1,2,3])
    [-1.224744871391589, 0.0, 1.224744871391589]
    """
    return list(zscore(values))
