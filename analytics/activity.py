from typing import List
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


def frequently_dotted_subjects(dots: List[objects.Dot],
                               min_percent_1: float = 0.10,
                               min_count_1: int = 0,
                               min_percent_2: float = 0.05,
                               min_count_2: int = 5) -> List[objects.Judgement]:
    """
    * Determines whether a Subject is Frequently Dotted: receives more than either:
    * 10% of all Dot Ratings OR
    * 5% of all Dot Ratings along with 10 Dot Ratings.

    TODO: Reconcile with Primary Participants

    Parameters
    ----------
    dots

    Returns
    -------
    List[objects.Judgement]
        Determines whether each subject in a collection of Dots is frequently dotted.
    """
    subjects = set([dot.target for dot in dots])

    result = []
    for s in subjects:
        subject_dots = [dot for dot in dots if dot.source == s]
        cond1 = len(subject_dots) / len(dots) > min_percent_1 and len(subject_dots) > min_count_1
        cond2 = len(subject_dots) / len(dots) > min_percent_2 and len(subject_dots) > min_count_2
        frequently_dotted = cond1 or cond2
        subject_is_frequently_dotted = objects.Judgement(source=objects.System,
                                                         target=s,
                                                         value=frequently_dotted)
        result += [subject_is_frequently_dotted]

    return result
