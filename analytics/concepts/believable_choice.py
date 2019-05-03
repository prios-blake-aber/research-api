import itertools
import numpy as np
from typing import Tuple, List, TypeVar, Optional
from analytics import foundation, utils
from src import objects, meta


StringOrFloat = TypeVar("StringOrFloat", str, float)
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
        Value or None
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
