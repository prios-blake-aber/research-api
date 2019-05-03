from typing import List
from src import objects, meta
from analytics import utils
from typing import List, Any

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
def quorum_exists_on_question_145(question: objects.Question, number_participants, quorum_threshold):
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
        quorum_flag = (number_responses / number_participants > quorum_threshold) and (number_responses > 3)
        return meta.Assertion(source=objects.System, target=question, value=quorum_flag, measure=objects.BooleanOption)
    else:
        return meta.Assertion(source=objects.System, target=question, value=None, measure=objects.BooleanOption)


def engagement(values: List[Any]):
    return len(values)


def engagement_in_meeting(meeting: objects.Meeting):
    return engagement(meeting.participants.data)


def engagement_in_question(question: objects.Question):
    return engagement(question.responses.data)


def sufficient_question_engagement(question: objects.Question):
    total_responses = engagement_in_question(question)
    sufficient_engagement_flag = total_responses > 3
    return sufficient_engagement_flag


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


def primary_participants(dots: List[objects.Dot]) -> List[objects.Judgement]:
    """
    Primary participants.

    # TODO: Identical to `insights.activity.primary_participants_in_meeting_138`?
    # TODO: Is it an insight or an analytic?

    Parameters
    ----------
    dots

    Returns
    -------
    List[objects.Judgement]
        True/False for whether people are a participant.
    """
    pass


def notable_participants(meeting: objects.Meeting, **kwargs) -> List[objects.Judgement]:
    """
    Returns True/False for whether a list of Participants in a Meeting are Notable Participants.
    Notable Participants are:
    * Believable
    * Primary Participant

    Parameters
    ----------
    meeting
    kwargs

    Returns
    -------
    List of people who are primary or believable.
    """

    # TODO: General utility function for filtering lists on some variable.
    believable_people = [person for person in meeting.participants if person.believability > 0]

    primary_people = primary_participants(meeting.dots)

    return combine_results(believable_people, primary_people, condition="OR")


def combine_results(*args):
    """
    Determines whether values are True in two (or more) lists of
    Judgements. Elements of each list should have the same targets, which only appear once.

    Not an insight (just a placeholder)

    # TODO: Find better home.
    # TODO: Is this a utils for analytics OR insights? See insights.disagreements.combine_results
    Parameters
    ----------
    args

    Returns
    -------

    """
    pass
