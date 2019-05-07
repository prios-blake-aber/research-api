from typing import List, Callable, Optional
from prios_api.src import foundation


def synthesize(values: List[float],
               synthesis_fun: Callable = foundation.weighted_average) -> Optional[float]:
    """
    Synthesize values into a
    Parameters
    ----------
    values
        Numerical values that are being synthesized into a single number.
    synthesis_fun
        Operation applied to synthesize a list of values.

    Returns
    -------
    float
        Synthesized value. Returns None if there aren't any values.

    Examples
    --------
    >>> synthesize([])
    >>> synthesize([1, 1, 1, 2, 5])
    2.0
    >>> import numpy as np
    >>> synthesize([1, 1, 1, 2, 5], np.median)
    1.0
    """
    if len(values) < 1:
        return None
    return synthesis_fun(values)
