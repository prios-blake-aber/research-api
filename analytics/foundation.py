from typing import List, Callable, Optional
import numpy as np
from src import objects


def map_values(x: List[float], from_type: objects.NumericRange):
    """
    Maps values from one numeric range to a different numeric range.

    TODO: Add parameter for mapping lambda and to_type.
    TODO: Hard-coded to map 1-to-10 or 1-to-5 values to "Semantic Buckets".

    Parameters
    ----------
    x
        Input data
    from_type

    Returns
    -------
    List[float]
        Numeric values on different scale. Currently hard-coded to legacy semantic bucket scale.
    """
    if from_type == objects.NumericRange.ONE_TO_TEN:
        (low_thresh, high_thresh) = (5, 7)
    elif from_type == objects.NumericRange.ONE_TO_FIVE:
        (low_thresh, high_thresh) = (2.5, 3.5)
    else:
        return x

    return np.digitize(x, [low_thresh, high_thresh])


def standard_deviation(x: List[float]) -> float:
    return np.nanstd(np.array(x))


def weighted_average(values: List[float], weights: List[float]) -> float:
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
