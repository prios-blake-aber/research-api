"""
Engagement
"""

from typing import List, Any


def engagement_raw(values: List[Any]) -> float:
    """
    Calculate raw engagement level as the number of times an event occurred.

    Parameters
    ----------
    values
        List of values

    Returns
    -------
    float
        Engagement level (raw): the number of times an event occurred.

    Examples
    --------
    >>> engagement_raw([])
    0
    >>> engagement_raw([1, 1])
    2
    """
    return len(values)


def engagement_relative(values: List[Any], max_number_of_values: int) -> float:
    """
    Calculate engagement level as the percentage of times an event occurred.

    Parameters
    ----------
    values
        List of values
    max_number_of_values
        Maximum number of values: integer greater than or equal to max(1, `len(values)`)

    Returns
    -------
    float
        Engagement level (relative): percentage of times an event occurred

    Examples
    --------
    >>> engagement_relative([], 0)
    Traceback (most recent call last):
    ...
    ValueError: Maximum number of values must be >= to max(1, `len(values)`).
    >>> engagement_relative([1, 1], 1)
    Traceback (most recent call last):
    ...
    ValueError: Maximum number of values must be >= to max(1, `len(values)`).
    >>> engagement_relative([1, 1], 4)
    0.5
    """
    if max_number_of_values < max(1, len(values)):
        raise ValueError("Maximum number of values must be >= to max(1, `len(values)`).")
    return len(values) / max_number_of_values


def quorum_exists(values: List[Any], number_participants, quorum_threshold) -> bool:
    """
    TODO: generalize the concept of minimum_engagement
    Whether a quorum exists within a set of meta.objects.Judgements

    Parameters
    ----------
    values: any meta.objects.Judgements
    number_participants:
    quorum_threshold: The threshold above which quorum exists. Defaults to :data:`_QUORUM_THRESH_DEFAULT`

    Returns
    -------
    bool
        Whether a quorum exists within the set of values.
    """
    if number_participants:
        engagement_on = engagement_raw(values)
        quorum_flag = (engagement_on / number_participants > quorum_threshold) and (engagement_on > 3)
        return quorum_flag
    else:
        return None

