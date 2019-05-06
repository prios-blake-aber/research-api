
"""
TBD
"""

import itertools
import numpy as np
from typing import Tuple, List, TypeVar, Optional, Any
from analytics import foundation, utils
from src import objects, meta


StringOrFloat = TypeVar("StringOrFloat", str, float)
_THRESHOLD_HIGH = 1.7
_THRESHOLD_STD_SCALE = 1.0
_THRESHOLD_STD_MAPPED_SCALE = 0.5
_THRESHOLD_POLES = 0.25
_MINIMUM_THRESH = 0.7


def believable_choice(values_and_weights: List[Tuple[StringOrFloat, float]],
                      value_type: objects.QuestionType) -> Optional[StringOrFloat]:
    """
    Believable choice

    TODO: Change to ValueType.

    Parameters
    ----------
    values_and_weights
        Values and Believability weights.
    value_type
        Type of value

    Returns
    -------
    Optional[StringOrFloat]
        Value or None. Value represents either the believability-weighted average or the answer choice on which there is
         sufficient believability.
    """

    total_believability = sum([x[1] for x in values_and_weights])

    if not total_believability:
        return None

    if value_type in [objects.QuestionType.LIKERT, objects.QuestionType.SCALE]:
        return believable_choice_numeric(values_and_weights)
    elif value_type in [objects.QuestionType.CATEGORICAL, objects.QuestionType.BINARY]:
        return believable_choice_categorical_binary(values_and_weights)
    else:
        return None


def believable_choice_numeric(values_and_weights: List[Tuple[float, float]]) -> float:
    """
    "Believable Choice" logic for Numeric responses.

    Parameters
    ----------
    values_and_weights
        Numeric values and corresponding believability.

    Returns
    -------
    float
        Believability-weighted average
    """
    values = [x[0] for x in values_and_weights]
    weights = [x[1] for x in values_and_weights]
    return foundation.weighted_average(values, weights)


def believable_choice_categorical_binary(values_and_weights: List[Tuple[str, float]],
                                         minimum_vote: float = _MINIMUM_THRESH) \
        -> Optional[str]:
    """
    Disagrees With logic for Categorical/Binary responses.

    Parameters
    ----------
    values_and_weights
        Strings values and corresponding believability
    minimum_vote
        Believable choice has greater than this quantity of the believability-weighted vote.

    Returns
    -------
    Optional[str]
        Believable choice, or None (if there isn't one).
    """
    vote = foundation.percent_of_total(values_and_weights)
    for key, value in vote:
        if value > minimum_vote:
            return key
    return None


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


def is_polarizing(scale_assertions: objects.ScaleValueSet,
                  thresh_on_std_scale: float = _THRESHOLD_STD_SCALE,
                  thresh_on_std_mapped_scale: float = _THRESHOLD_STD_MAPPED_SCALE,
                  thresh_on_poles: float = _THRESHOLD_POLES) -> objects.Judgement:

    """
    Parameters
    ----------
    scale_assertions
        List of assertions with scale values.
    thresh_on_std_scale
        Threshold on standard deviation of scale values.
    thresh_on_std_mapped_scale
        Threshold on standard deviation of scale values mapped to 1, 2, and 3
    thresh_on_poles
        Threshold on ratio between poles

    Returns
    -------
    object.Judgement
        Whether a set of scale values are polarizing.
    """
    values = [xi.value for xi in scale_assertions.data]
    mapped_values = [foundation.map_values(vi, objects.NumericRange.ONE_TO_TEN) for vi in values]

    # TODO: nesting functions here is terrible; why not use the sentiment module?
    def negative_sentiment(x):
        return x == 1

    def positive_sentiment(x):
        return x == 3

    percent_negative = foundation.percent_satisfying_condition(mapped_values, negative_sentiment)
    percent_positive = foundation.percent_satisfying_condition(mapped_values, positive_sentiment)

    if percent_negative > 0 and percent_positive > 0:
        pole_ratio = min(percent_positive/percent_negative, percent_negative/percent_positive)
    else:
        pole_ratio = 0

    std_values_condition = foundation.standard_deviation(values) > thresh_on_std_scale
    std_mapped_values_condition = foundation.standard_deviation(mapped_values) > thresh_on_std_mapped_scale
    pole_condition = pole_ratio > thresh_on_poles
    result = std_values_condition and std_mapped_values_condition and pole_condition
    return objects.Judgement(source=objects.System, target=objects.System, value=result)


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
    categorical_binary = question_type in (objects.QuestionType.CATEGORICAL, objects.QuestionType.BINARY)
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
