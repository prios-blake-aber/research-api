
"""
TBD
"""

import itertools
from prios_api.domain_objects import meta, objects
from prios_api.src import utils
from prios_api import activity
from typing import List

_QUORUM_THRESH_DEFAULT = 0.80


def primary_actions_157(dots: objects.DotCollection, *args, **kwargs):
    """
    Defines Primary Actions in a Meeting based on :class:`objects.DotCollection`

    Parameters
    ----------
    dots
        A set of :class:`objects.Dot`.
    args
    kwargs

    Returns
    -------
    objects.RelevanceCollection
         A set of :class:`objects.RelevanceScore`, or an empty set if none exist.
    """
    relevant_actions = action_relevance_158(dots)
    return sorted(relevant_actions, key=lambda x: x.value)[:3]  # top 3 scores


def primary_participants_in_meeting_138(meeting: objects.Meeting,
                                        min_percent_1: float = 0.20,
                                        min_count_1: int = 0,
                                        min_percent_2: float = 0.10,
                                        min_count_2: int = 10,
                                        *args, **kwargs) -> List[meta.Assertion]:
    """
    Defines Primary Participants in a Meeting from Dots.

    Parameters
    ----------
    dots
    min_percent_1
        A subject is a Primary Participant if the percent of dots they receive exceeds this quantity
        and the number of dots exceeds `min_count_1` (default = 10%)
    min_count_1
        A subject is a Primary Participant if the number of dots they receive exceeds this quantity
        and the percentage of dots exceeds `min_percent_1` (default = 0)
    min_percent_2
        A subject is a Primary Participant if the percent of dots they receive exceeds this quantity
        and the number of dots exceeds `min_count_2` (default = 5%)
    min_count_2
        A subject is a Primary Participant if the number of dots they receive exceeds this quantity
        and the percentage of dots exceeds `min_percent_2` (default = 5)
    *args
        Variable length argument list.
    **kwargs
        Arbitrary keyword arguments.

    Returns
    -------
    List[meta.Assertion]
        System assertion for each subject with value (Boolean) equal to True if they are
        a Primary Participant or False, otherwise.
    """
    return activity.frequently_dotted_subjects(meeting.dots, min_percent_1, min_count_1,
                                               min_percent_2, min_count_2)


def action_relevance_158(dots: objects.DotCollection, *args, **kwargs):
    """
    Defines Action Relevance in a Meeting from Dots.

    Parameters
    ----------
    dots
    *args
        Variable length argument list.
    **kwargs
        Arbitrary keyword arguments.


    Returns
    -------
    objects.RelevanceCollection
         A set of :class:`objects.RelevanceScore`, or an empty set if none exist.
    """
    return activity.relevance_of_dots(dots)


def attention_participant_received_155(dots: objects.DotCollection):
    """
    Defines "Relevant" People in a Meeting from Dots.

    Parameters
    ----------
    dots
    *args
        Variable length argument list.
    **kwargs
        Arbitrary keyword arguments.


    Returns
    -------
    objects.RelevanceCollection
         A set of :class:`objects.RelevanceScore`, or an empty set if none exist.
    """
    return activity.relevance_of_people(dots)


@utils.scope_required_data_within_object(collections_to_keep=['participants', 'questions'])
def quorum_exists_on_question_145(meeting: objects.Meeting,
                                  quorum_threshold: float = _QUORUM_THRESH_DEFAULT,
                                  *args, **kwargs) -> List[meta.Assertion]:
    """
    Determines whether a sufficient percentage of Participants answered each question
    asked during a Meeting.

    Parameters
    ----------
    meeting
    quorum_threshold : The threshold above which quorum exists. Defaults to :data:`_QUORUM_THRESH_DEFAULT`
    *args: Variable length argument list.
    **kwargs: Arbitrary keyword arguments.

    Returns
    -------
    List[meta.Assertion]
        List of Assertions where each item is a Question and the Value is True if Quorum exists on respective question.
    """
    number_participants = activity.engagement_in_meeting(meeting)
    return [
        activity.quorum_exists_question(question, number_participants=number_participants,
                                        quorum_threshold=quorum_threshold)
        for question in meeting.questions.data
    ]

