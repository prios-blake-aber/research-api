
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


def select_participants_from_meeting(original_function):
    """This decorator selects Participants from the Meeting object and
    passes it into the decorated function"""
    def new_function(meeting, *args,**kwargs):
        participants = meeting.participants.data
        return original_function(participants, *args,**kwargs)
    return new_function


def select_responses_from_question(original_function):
    """This decorator selects Participants from the Meeting object and
    passes it into the decorated function"""
    def new_function(question, *args,**kwargs):
        responses = question.responses.data
        return original_function(responses, *args,**kwargs)
    return new_function


