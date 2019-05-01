from analytics import utils
from src import objects
"""
Analytics on Activities
"""


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


@utils.scope_required_data_within_object(collections_to_keep=['responses'])
def quorum_exists_on_question(question: objects.Question, number_participants, quorum_threshold):
    """
    Quorum of Responses on a Question.

    Parameters
    ----------
    question
    number_participants
    quorum_threshold

    Returns
    -------

    """
    if number_participants:
        number_responses = len(question.responses.data)
        quorum_flag = number_responses / number_participants > quorum_threshold
        return objects.IsQuorum(source=objects.System, target=question, value=quorum_flag)
    else:
        return objects.IsQuorum(source=objects.System, target=question, value=None)
