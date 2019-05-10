
"""
TBD
"""

from typing import Tuple, TypeVar, Any
from prios_api.src import foundation
from prios_api.domain_objects import meta, objects
from prios_api.concepts import believable_choice

StringOrFloat = TypeVar("StringOrFloat", str, float)
QuestionOrNumeric = TypeVar("QuestionOrNumeric", objects.QuestionType, objects.NumericRange)
_THRESHOLD_HIGH = 1.7
_THRESHOLD_STD_SCALE = 1.0
_THRESHOLD_STD_MAPPED_SCALE = 0.5
_THRESHOLD_POLES = 0.25
_MINIMUM_THRESH = 0.7


def disagrees_with_167(values : Tuple[Any, Any], value_type: QuestionOrNumeric) -> bool:
    """
    TODO need to handle the Value Type case better, consider Alex's new solution.

    Whether or not two values disagree.

    Parameters
    ----------
    values
        Input data
    value_type
        Type of values

    Returns
    -------
    Boolean
        True, if there is a disagreement.

    Examples
    --------
    >>> disagrees_with_167(('yes', 'no'), objects.QuestionType.BINARY)
    True
    >>> disagrees_with_167(('no', 'no'), objects.QuestionType.BINARY)
    False
    >>> disagrees_with_167((5, 7), objects.QuestionType.SCALE)
    True
    >>> disagrees_with_167((6, 7), objects.QuestionType.SCALE)
    False
    """
    x1, x2 = values
    categorical_binary = value_type in (objects.QuestionType.CATEGORICAL, objects.QuestionType.BINARY)
    numeric = value_type in (objects.QuestionType.LIKERT, objects.QuestionType.SCALE, objects.NumericRange)

    if categorical_binary:
        return x1 != x2
    elif numeric:
        return disagrees_with_numeric(x1, x2)
    else:
        return None


def disagrees_with_numeric(x1: float, x2: float, far_away: float=_THRESHOLD_HIGH) -> bool:
    """
    Disagrees With logic for Scale values (1-to-10 or 1-to-5).

    Parameters
    ----------
    x1: the value to compare to x2
    x2: the value to compare to x1
    far_away: the threshold at which two responses are deemed to be sufficiently different.

    Returns
    -------
    Boolean
        True, if there is a disagreement.

    Examples
    --------
    >>> disagrees_with_numeric(5, 7)
    True
    >>> disagrees_with_numeric(6, 7)
    False
    """
    mapped_x1, mapped_x2 = foundation.map_values([x1, x2], objects.NumericRange)
    same_bucket = mapped_x1 == mapped_x2

    try:
        far_away = abs(mapped_x1 - mapped_x2) > far_away

        return far_away and not same_bucket

    except TypeError:
        return not same_bucket


def bucketed_disagreement(x1: float, x2: float) -> float:
    """
    Parameters
    ----------
    values
        Tuple of numeric values

    Returns
    -------
    float
        The absolute difference in bucketed disagreement between two v alues.
    """
    mapped_x1, mapped_x2 = foundation.map_values([x1, x2], objects.NumericRange.ONE_TO_TEN)
    result = abs(mapped_x1 - mapped_x2)
    return result.item()  # TODO: handling of numpy conversion here is terrible


def substantive_disagreement(x1: float, x2: float, threshold_high: float = _THRESHOLD_HIGH):
    """
    Parameters
    ----------
    x1
        numeric value
    x2
        numeric value
    threshold_high
        Returns False if difference between raw values is less than this quantity.

    Returns
    -------
    bool
        Whether there's substantive disagreement between two values.
    """
    diff = abs(x1 - x2)
    far_away = diff > threshold_high
    mapped_diff = bucketed_disagreement(x1, x2)
    return far_away and mapped_diff


