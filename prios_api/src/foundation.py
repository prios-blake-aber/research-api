
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
QuestionOrNumeric = TypeVar("QuestionOrNumeric", objects.QuestionType, objects.NumericRange)
YES_VALUE = 2
NO_VALUE = 1


def map_values(values: List[StringOrFloat], value_type: QuestionOrNumeric):
    """
    Maps values from one numeric range to a different numeric range. Currently, mapping is to
    defined for 1-to-10 or 1-to-5 ranges to "Semantic Buckets" (Positive, Negative, or Neutral).

    TODO: Add parameter for mapping lambda and to_type.
    TODO: Hard-coded to map 1-to-10 or 1-to-5 values to "Semantic Buckets".
    TODO: Need to consider adopting Alex's typing system (Yes/No handling is currently not great).

    Parameters
    ----------
    values
        Input data
    value_type
        Type of values

    Returns
    -------
    List[float]
        Numeric values on different scale. Currently hard-coded to legacy semantic bucket scale.

    Examples
    --------
    >>> print(map_values([1, 2, 3, 4, 5], value_type=objects.QuestionType.LIKERT))
    [0 0 1 2 2]
    >>> print(map_values([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], value_type=objects.QuestionType.SCALE))
    [0 0 0 0 1 1 2 2 2 2]
    >>> print(map_values(["Yes", "No", "Yes", "No"], value_type=objects.QuestionType.BINARY))
    [2, 1, 2, 1]
    >>> print(map_values(['Give up', 'Push Ahead and see what happens', 'Delay',
    ...                  'Do whatever it takes to make it work'], value_type=objects.QuestionType.CATEGORICAL))
    ['Give up', 'Push Ahead and see what happens', 'Delay', 'Do whatever it takes to make it work']
    """

    # TODO: Finalize value-type object.
    if value_type == objects.NumericRange.ONE_TO_TEN:
        value_type = objects.QuestionType.SCALE
    if value_type == objects.NumericRange.ONE_TO_FIVE:
        value_type = objects.QuestionType.LIKERT
    if value_type == objects.QuestionType.BINARY:
        value_type = objects.QuestionType.BINARY

    if value_type == objects.QuestionType.BINARY:
        return [YES_VALUE if x == "Yes" else NO_VALUE for x in values]
    elif value_type == objects.QuestionType.SCALE:
        (low_thresh, high_thresh) = (5, 7)
    elif value_type == objects.QuestionType.LIKERT:
        (low_thresh, high_thresh) = (2.5, 3.5)
    else:
        return values

    return np.digitize(values, [low_thresh, high_thresh])


def standard_deviation(x: List[float]) -> float:
    """
    Parameters
    ----------
    x
        Input values, list of floats

    Returns
    -------
    Float
        Standard deviation of the list of values

    Examples
    --------
    >>> print(round(standard_deviation([1, 2, 4, 4, 4]), 2))
    1.41
    >>> print(round(standard_deviation([1]), 2))
    nan
    """
    return np.nanstd(np.array(x), ddof=1)


def weighted_average(values: List[float], weights=None) -> float:
    """
    Average of numeric values.

    Parameters
    ----------
    values
        List of numeric values
    weights
        List of numeric values

    Returns
    -------
    float

    Examples
    --------
    >>> round(weighted_average([2, 1, 4, 4, 4], weights=[0.2, 0.01, 0.3, 0, 0]), 3)
    3.157
    >>> round(weighted_average([2, 1, 4, 4, 4], weights=None))
    3.0
    >>> round(weighted_average(3, weights=None))
    3.0
    >>> round(weighted_average(3, weights=0.2))
    3.0
    """
    return np.average(values, weights=weights)


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

    Examples
    --------
    >>> percent_of_total([])
    {}
    >>> percent_of_total([('yes', 0.05), ('no', 0.95)])
    {'no': 0.95, 'yes': 0.05}
    >>> percent_of_total([('yes', 5), ('no', 95)])
    {'no': 0.95, 'yes': 0.05}
    """
    total = sum([x[1] for x in values_and_weights])
    sorted_responses = sorted(values_and_weights, key=lambda x: x[0])
    result = dict()
    for choice, weight in itertools.groupby(sorted_responses, key=lambda x: x[0]):
        sum_weights = sum([x[1] for x in weight])
        result[choice] = sum_weights / total
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
