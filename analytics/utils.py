from typing import List
from src import objects
import numpy as np


def group_assertions_by_criteria(x: objects.AssertionSet):
    """
    TODO: Define generalization for grouping summary data

    This function is a catch-all for the multiple grouping
    functions that exist for summaries
    """
    pass


def select_dots_from_meeting(original_function):
    """This decorator selects dots from the Meeting object and
    passes it into the decorated function"""
    def new_function(meeting, *args,**kwargs):
        dots = meeting.dots.data
        return original_function(dots, *args,**kwargs)
    return new_function


def scope_required_data_within_object(attributes_to_keep=None, collections_to_keep=None):
    """This decorator scopes the required data for an object
    and passes it into the decorated function"""
    def actual_filtering_decorator(function):
        def wrapper(original_object, **kwargs):
            original_object.empty(attributes_to_keep, collections_to_keep)
            print(dir(original_object))
            return function(original_object, **kwargs)
        return wrapper
    return actual_filtering_decorator


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
