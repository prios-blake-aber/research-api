
from src import objects, meta
from analytics import utils

"""
Analytics on Activities
"""

_QUORUM_THRESH_DEFAULT = 0.80

def relevance(dots: objects.AssertionSet):
    """
    Defines a “Relevance” score for each :class:`objects.Assertion` as a function of the number of of relevant Dots given.

    Args:
        dots (objects.AssertionSet): A set of :class:`objects.Assertion`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.AssertionSet: A set of relevant :class:`objects.Assertion`, or an empty set if none exist.
    """
    pass


def relevance_of_dots(dots: objects.DotCollection):
    """
    Defines a “Relevance” score for each :class:`objects.Attribute` as a function of the number of of relevant Dots given.

    Args:
        dots (objects.DotCollection): A set of :class:`objects.Dot`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.RelevanceCollection: A set of :class:`objects.RelevanceScore`, or an empty set if none exist.
    """
    pass


def relevance_of_people(dots: objects.DotCollection):
    """
    Defines a “Relevance” score for each :class:`objects.Person` as a function of the number of of relevant Dots given.

    Args:
        dots (objects.DotCollection): A set of :class:`objects.Dot`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.RelevanceCollection: A set of :class:`objects.RelevanceScore`, or an empty set if none exist.
    """
    pass

@utils.scope_required_data_within_object(collections_to_keep=['participants', 'questions'])
def quorum_exists_in_meeting(meeting: objects.Meeting):
    """
    Defines a "Quorum" for each :class:`objects.Questions` as a function of the number of Meeting Participants and Question Responses. https://github.principled.io/vgs/core-access/tree/master/docs/analytic-implementations/83357bac-d082-4085-8fda-07ade37bfb86.pdf

    Args:
        meeting (objects.Meeting): A set of :class:`objects.Assertion`.
        quorum_threshold : The threshold above which quorum exists. Defaults to :data:`_QUORUM_THRESH_DEFAULT`
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        bool : Whether quorum exists. Returns None if num_participants is 0.
    """

    number_participants = len(meeting.participants.data)
    return [
        quorum_exists_on_question(question, number_participants=number_participants)
        for question in meeting.questions.data
    ]


@utils.scope_required_data_within_object(collections_to_keep=['responses'])
def quorum_exists_on_question(question: objects.Question, number_participants, quorum_threshold = _QUORUM_THRESH_DEFAULT):
    """
    INSERT DOCSTRING HERE
    """
    if number_participants:
        number_responses = len(question.responses.data)
        quorum_flag = number_responses / number_participants > quorum_threshold and number_responses > 3
        return meta.Assertion(source=objects.System, target=question, value=quorum_flag, measure=objects.BooleanOption)
    else:
        return meta.Assertion(source=objects.System, target=question, value=None, measure=objects.BooleanOption)
