"""
Engagement
"""

from typing import List, Any


def engagement_raw(values: List[Any], believability_weighted=False) -> float:
    """
    Calculate raw engagement level as the number of times an event occurred.

    Parameters
    ----------
    values
        List of values

    believability_weighted
        Whether or not engagement should be measured as the amount of Believability present. If true will return the
        sum of Believabilities associated with the values passed in.

    Returns
    -------
    float
        Engagement level (raw): the number of times an event occurred, or, if believability_weighted is True, the sum
        of Believabilities associated with the values passed in.

    Examples
    --------
    >>> engagement_raw([])
    0
    >>> engagement_raw([1, 1])
    2
    """
    if believability_weighted:
        return sum(values)
    else:
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

