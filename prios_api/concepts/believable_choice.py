"""
Believable Choice.
"""

from typing import Tuple, List, TypeVar, Optional
from prios_api.src import foundation
from prios_api.domain_objects import objects

StringOrFloat = TypeVar("StringOrFloat", str, float)
_THRESHOLD_HIGH = 1.7
_THRESHOLD_STD_SCALE = 1.0
_THRESHOLD_STD_MAPPED_SCALE = 0.5
_THRESHOLD_POLES = 0.25
_MINIMUM_THRESH = 0.7


def believable_choice_categorical_binary(values_and_weights: List[Tuple[str, float]],
                                         minimum_vote: float = _MINIMUM_THRESH) -> Optional[str]:
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

    Examples
    --------
    >>> from prios_api.examples import binaryexample
    >>> print(believable_choice_categorical_binary(binaryexample.values_and_weights))
    No
    >>> from prios_api.examples import categoricalexample
    >>> print(believable_choice_categorical_binary(categoricalexample.values_and_weights))
    None
    >>> from prios_api.examples import singleresponseexample
    >>> print(believable_choice_categorical_binary(singleresponseexample.values_and_weights))
    1
    """
    vote = foundation.percent_of_total(values_and_weights)
    for key, value in vote.items():
        if value > minimum_vote:
            return key
    return None


