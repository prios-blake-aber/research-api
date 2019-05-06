
"""
TBD
"""

from typing import Tuple, TypeVar, Any
from prios_api.utils import foundation
from prios_api.domain_objects import meta, objects

StringOrFloat = TypeVar("StringOrFloat", str, float)
_THRESHOLD_HIGH = 1.7
_THRESHOLD_STD_SCALE = 1.0
_THRESHOLD_STD_MAPPED_SCALE = 0.5
_THRESHOLD_POLES = 0.25
_MINIMUM_THRESH = 0.7


def disagrees_with_167(values : Tuple[Any, Any], question_type) -> meta.Assertion:
    """
    Significantly OOS, etc.

    Parameters
    ----------
    values
    question_type

    Returns
    -------
    objects.AssertionSet
        Empty set, if none exists.
    """
    response, response_value = values
    categorical_binary = question_type in (
    objects.QuestionType.CATEGORICAL, objects.QuestionType.BINARY)
    numeric = question_type in (objects.QuestionType.LIKERT, objects.QuestionType.SCALE)

    if categorical_binary:
        return disagrees_with_categorical_binary(response, response_value)
    elif numeric:
        return disagrees_with_numeric(response, response_value)
    else:
        return None


def disagrees_with_categorical_binary(response_to_compare: StringOrFloat,
                                      answer_to_compare: StringOrFloat) -> meta.Assertion:
    """
    Disagrees With logic for Categorical/Binary values.

    TODO: Find better home -> is this a core concept?

    Parameters
    ----------
    response_to_compare
    answer_to_compare

    Returns
    -------
    meta.Assertion
        Value is True, if there is a disagreement.
    """
    result = response_to_compare != answer_to_compare
    return meta.Assertion(source=objects.System, target=response_to_compare, value=result,
                          measure=objects.BooleanOption)


def disagrees_with_numeric(response_to_compare: float,
                           answer_to_compare: float,
                           far_away: float=_THRESHOLD_HIGH) -> meta.Assertion:
    """
    Disagrees With logic for Scale values (1-to-10 or 1-to-5).

    TODO: Find better home -> is this a core concept?

    Parameters
    ----------
    response_to_compare
    answer_to_compare

    Returns
    -------
    meta.Assertion
        Value is True, if there is a disagreement.
    """
    buckets = foundation.map_values([response_to_compare, answer_to_compare], objects.NumericRange)
    same_bucket = buckets[0] == buckets[1]

    try:
        far_away = abs(response_to_compare - answer_to_compare) > far_away

        result = far_away and not same_bucket
        return meta.Assertion(source=objects.System, target=response_to_compare, value=result,
                              measure=objects.FloatOption)

    except TypeError:
        return not same_bucket


def substantive_disagreement(scale_values: Tuple[float, float],
                             threshold_high: float = _THRESHOLD_HIGH):
    """
    Parameters
    ----------
    scale_values
        Scale Value Pair
    threshold_high
        Returns False if difference between raw values is less than this quantity.

    Returns
    -------
    object.Judgement
        Whether there's substantive disagreement between two assertions.
    """
    x1, x2 = scale_values
    diff = abs(x1.value - x2.value)
    far_away = diff > threshold_high
    mapped_x1 = foundation.map_values(x1.value, objects.NumericRange.ONE_TO_TEN)
    mapped_x2 = foundation.map_values(x2.value, objects.NumericRange.ONE_TO_TEN)
    mapped_diff = abs(mapped_x1 - mapped_x2)
    result = far_away and mapped_diff
    return result

