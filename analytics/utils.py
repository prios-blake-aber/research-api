
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
