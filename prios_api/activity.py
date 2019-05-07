
"""
PRIOS Analytics on Activity.
"""

from typing import List
from prios_api.domain_objects import meta, objects
from prios_api.src import utils, foundation
from prios_api.concepts import engagement, ungrouped


_QUORUM_THRESH_DEFAULT = 0.80
_SUFFICIENT_RESPONSE_ENGAGEMENT = 3
_SUFFICIENT_BELIEVABILITY_ENGAGEMENT = 0.75


def relevance_of_dots(dots: List[objects.Dot]):
    pass


def relevance_of_people(dots: List[objects.Person]):
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
    return engagement.engagement_raw(meeting.participants.data)


def engagement_in_question(question: objects.Question):
    return engagement.engagement_raw(question.responses.data)


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
    individual_believability = [response.source.believability for response in question.responses]
    total_believability = foundation.addition(individual_believability)
    if total_believability > believability_engagement:
        return True
    else:
        return False


def frequently_dotted_subjects(dots: List[objects.Dot],
                               min_percent_1: float = 0.10,
                               min_count_1: int = 0,
                               min_percent_2: float = 0.05,
                               min_count_2: int = 5) -> List[meta.Assertion]:
    """
    Determines whether a Subject is Frequently Dotted. receives more than either:
    * 10% of all Dot Ratings OR
    * 5% of all Dot Ratings along with 10 Dot Ratings.


    Parameters
    ----------
    dots
    min_percent_1
        A subject is frequently dotted if the percent of dots they receive exceeds this quantity
        and the number of dots exceeds `min_count_1` (default = 10%)
    min_count_1
        A subject is frequently dotted if the number of dots they receive exceeds this quantity
        and the percentage of dots exceeds `min_percent_1` (default = 0)
    min_percent_2
        A subject is frequently dotted if the percent of dots they receive exceeds this quantity
        and the number of dots exceeds `min_count_2` (default = 5%)
    min_count_2
        A subject is frequently dotted if the number of dots they receive exceeds this quantity
        and the percentage of dots exceeds `min_percent_2` (default = 5)

    Returns
    -------
    List[meta.Assertion]
        System assertion for each subject with value (Boolean) equal to True if they are
        frequently dotted or False, otherwise.
    """
    subjects = set([dot.target for dot in dots])

    result = []
    for s in subjects:
        subject_dots = [dot for dot in dots if dot.source == s]
        percent_dots = engagement.engagement_relative(subject_dots, len(dots))
        total_dots = engagement.engagement_raw(subject_dots)
        cond1 = percent_dots > min_percent_1 and total_dots > min_count_1
        cond2 = percent_dots > min_percent_2 and total_dots > min_count_2
        subject_is_frequently_dotted = meta.Assertion(source=objects.System,
                                                      target=s,
                                                      value=cond1 or cond2)
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
