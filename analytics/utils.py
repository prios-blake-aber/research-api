
from src import objects


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


def select_participants_and_responses_from_meeting(original_function):
    """This decorator selects dots from the Meeting object and
    passes it into the decorated function"""
    def new_function(meeting, *args,**kwargs):
        participants = meeting.participants.data
        questions = meeting.questions.data

        meeting.empty()
        meeting.participants = participants
        meeting.questions = questions
        return original_function(meeting, *args,**kwargs)
    return new_function


def scope_required_data_within_object(
        attributes_to_keep=None, collections_to_keep=None
):
    """This decorator scopes the required data for an object
    and passes it into the decorated function"""
    assert (not attributes_to_keep) | (not collections_to_keep), 'Must specify some data to retain in object!'

    def actual_filtering_decorator(function):
        def wrapper(original_object, **kwargs):
            modified_object = original_object.empty(
                attributes_to_keep, collections_to_keep
            )
            return function(modified_object, **kwargs)
        return wrapper
    return actual_filtering_decorator
