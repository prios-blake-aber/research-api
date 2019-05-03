import itertools
import numpy as np
from typing import Tuple, List, TypeVar, Optional
from analytics import foundation, utils
from src import objects, meta


StringOrFloat = TypeVar("StringOrFloat", str, float)


def believable_choice(ar: List[StringOrFloat]) -> Optional[StringOrFloat]:
    """
    Believable choice

    Parameters
    ----------
    ar
        Values

    Returns
    -------
    Optional[StringOrFloat]
        None if there no believable choice.
    """
pass
