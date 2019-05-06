
"""
TBD
"""

from typing import List
from prios_api.domain_objects import meta, objects
from prios_api import utils
from prios_api.utils import foundation
from prios_api.concepts import ungrouped


_QUORUM_THRESH_DEFAULT = 0.80
_SUFFICIENT_RESPONSE_ENGAGEMENT = 3
_SUFFICIENT_BELIEVABILITY_ENGAGEMENT = 0.75


def relevance_of_dots(dots: objects.DotCollection):
    pass


def relevance_of_people(dots: objects.DotCollection):
    pass


@utils.scope_required_data_within_object(collections_to_keep=['responses'])
def quorum_exists_question(question: objects.Question, number_participants, quorum_threshold):
    """
    Determines whether a sufficient percentage of Participants answered each question
    asked during a Meeting.

    Parameters
    ----------
    question
    number_participants
    quorum_threshold: The threshold above which quorum exists. Defaults to :data:`_QUORUM_THRESH_DEFAULT`

    Returns
    -------
    meta.Assertion
        A single assertion that where the value is True if a Quorum Exists on the Question or None if no Quorum exists.
    """
    quorum_flag = ungrouped.quorum_exists(question.responses.data, number_participants, quorum_threshold)
    if quorum_flag:
        return meta.Assertion(source=objects.System, target=question, value=quorum_flag, measure=objects.BooleanOption)
    else:
        return meta.Assertion(source=objects.System, target=question, value=None, measure=objects.BooleanOption)


def engagement_in_meeting(meeting: objects.Meeting):
    return ungrouped.engagement(meeting.participants.data)


def engagement_in_question(question: objects.Question):
    return ungrouped.engagement(question.responses.data)


def sufficient_believability_engagement(question: objects.Question,
                                        believability_engagement=_SUFFICIENT_BELIEVABILITY_ENGAGEMENT) -> bool:
    """
    TODO: Needs clarification on where it lives conceptually, what the I/O types should be, whether it can be refactored
    Determines whether there was enough Believability in the question responses.

    Parameters
    ----------
    question
    believability_engagement: threshold at which there is sufficient believability.
        Defaults at _SUFFICIENT_BELIEVABILITY_ENGAGEMENT

    Return
    ------
    Bool
        True if there is sufficient believability.
    """
    individual_believability = [response.source.believability for response in question.responses.data]
    total_believability = foundation.addition(individual_believability)
    if total_believability > believability_engagement:
        return True
    else:
        return False



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

    primary_people = ungrouped.primary_participants(meeting.dots)

    return combine_results(believable_people, primary_people, condition="OR")


def combine_results(*args):
    """
    Determines whether values are True in two (or more) lists of
    Judgements. Elements of each list should have the same targets, which only appear once.

    Not an insight (just a placeholder)

    # TODO: Find better home.
    # TODO: Is this a utils for prios_api OR insights? See insights.disagreements.combine_results
    Parameters
    ----------
    args

    Returns
    -------

    """
    pass