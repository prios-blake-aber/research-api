
"""
TBD
"""
import typing
from itertools import groupby
from prios_api.domain_objects import meta, objects


def group_assertions_by_key(
        assertions: typing.List[meta.Assertion], keyfunc: typing.Callable) -> \
        typing.List[typing.Tuple[typing.Any, typing.Any]]:
    """
    Groups values in list of assertions by user-specified Callable.

    Parameters
    ----------
    assertions
        List of assertions
    keyfunc
        Callable specifying groupby function

    Returns
    -------
    typing.List[typing.Tuple[typing.Any, typing.Any]]
        Each element of list is indexed by a defined group with a
        list of associated assertions.

    Examples
    --------
    >>> research = objects.Meeting(name='Research Meeting')
    >>> adam = objects.Person(name='Adam')
    >>> bob = objects.Person(name='Bob')
    >>> charlie = objects.Person(name='Charlie')
    >>> research.dots.append(objects.Dot(source=adam, target=bob, value=10))
    >>> research.dots.append(objects.Dot(source=adam, target=bob, value=5))
    >>> research.dots.append(objects.Dot(source=charlie, target=bob, value=1))
    >>> research.dots.append(objects.Dot(source=charlie, target=adam, value=5))
    >>> keyfunc = lambda x: (x.source.uuid, x.target.uuid)
    >>> result = group_assertions_by_key(research.dots, keyfunc=keyfunc)
    >>> for key, data in result:
    ...     for dot in data:
    ...         print(dot.source.name, dot.target.name, dot.value)
    Adam Bob 10
    Adam Bob 5
    Charlie Bob 1
    Charlie Adam 5
    """
    assertion_list = sorted(assertions, key=keyfunc)
    grouped_assertion_list = groupby(assertion_list, key=keyfunc)
    return [(k, list(v)) for k, v in grouped_assertion_list]


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


