
import itertools
import numpy as np
from src import objects, meta


def group_assertions_by_criteria(x: objects.AssertionSet):
    """
    TODO: Define generalization for grouping summary data

    This function is a catch-all for the multiple grouping
    functions that exist for summaries
    """
    pass


def believable_choice_numeric(question: objects.Question, total_believability=None):
    if not total_believability:
        result = None
    else:
        result = np.average(
            [response.value for response in question.responses.data],
            weights=[response.source.believability for response in question.responses.data]
        )
    return meta.Assertion(source=objects.System, target=question, value=result, measure=objects.FloatOption)


def believable_choice_categorical_binary(question: objects.Question, total_believability=None):
    if not total_believability:
        result = None
    else:
        result = None
        sorted_responses = sorted(question.responses.data, key=lambda x: x.value)
        for response_choice, response_set in itertools.groupby(sorted_responses, key=lambda x: x.value):
            if sum([i.source.believability for i in response_set]) / total_believability > 0.7:
                result = response_choice
    return meta.Assertion(source=objects.System, target=question, value=result, measure=objects.BooleanOption)


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
