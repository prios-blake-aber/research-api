
"""
TBD
"""
from typing import List, Tuple
from itertools import groupby
from src import meta
from prios_api.domain_objects import objects


def group_assertion_values_by_source_and_target(assertions: List[meta.Assertion]) -> List[Tuple[
    Tuple[objects.Person, objects.Person], List[float]]]:
    """
    Groups values in list of assertions by source and target.

    Parameters
    ----------
    assertions
        List of assertions

    Returns
    -------
    List[Tuple[Tuple[objects.Person, objects.Person], List[float]]]
        Each element of list is indexed by a Source-Target tuple of Person objects and with a
        list of associated values.

    Examples
    --------
    >>> Adam = objects.Person(name='Adam')
    >>> Bob = objects.Person(name='Bob')
    >>> Charlie = objects.Person(name='Charlie')
    >>> asserts = list()
    >>> asserts.append(meta.Assertion(source=Adam, target=Bob, value=10))
    >>> asserts.append(meta.Assertion(source=Adam, target=Bob, value=5))
    >>> asserts.append(meta.Assertion(source=Charlie, target=Bob, value=1))
    >>> asserts.append(meta.Assertion(source=Charlie, target=Adam, value=5))
    >>> result = group_assertion_values_by_source_and_target(asserts)
    >>> result_to_print = [((x[0][0].name, x[0][1].name), x[1]) for x in result]
    >>> result_to_print
    [(('Adam', 'Bob'), [10, 5]), (('Charlie', 'Bob'), [1]), (('Charlie', 'Adam'), [5])]
    """
    asserts = [
        {
            'source': a.source,
            'target': a.target,
            'value': a.value
        } for a in assertions
    ]
    asserts_group_by = groupby(asserts, key=lambda x: (x['source'], x['target']))
    return [
        (x[0], [y['value'] for y in list(x[1])]) for x in asserts_group_by
    ]


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


