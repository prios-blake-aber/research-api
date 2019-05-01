from typing import List
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
