
from src import objects


def group_assertions_by_criteria(x: objects.AssertionSet):
    """
    TODO: Define generalization for grouping summary data

    This function is a catch-all for the multiple grouping
    functions that exist for summaries
    """
    pass


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
