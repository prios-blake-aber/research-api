
"""
TBD
"""

import typing
from prios_api.src import foundation


def sentiment(values: typing.List[float], weights=None):
    """
    Defines sentiment as the average of all values

    Args:
        values (typing.List[float]): A list of :type:float.
        weights: Weights to apply as a weighted average.

    Returns:
        objects.Assertion: A value representing sentiment, or None.
    """
    return foundation.weighted_average(values, weights)
