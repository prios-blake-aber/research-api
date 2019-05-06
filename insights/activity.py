
"""
TBD
"""

import itertools
from src import objects, meta
from analytics import utils, activity
from typing import List, Any


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


def primary_participants_in_meeting_138(dots: objects.DotCollection, *args, **kwargs):
    """
    # TODO: Move logic to analytics.
    Defines Primary Participants in a Meeting from Dots.

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
    total_participation = len(dots)
    dots.sort(key=lambda x: x.source.name, reverse=False)
    for person, dots in itertools.groupby(dots, lambda x: x.target):
        person_dots = len(list(dots))
        if ((person_dots / total_participation) > 0.2) or (person_dots > 10 and ((person_dots / total_participation) > 0.1)):
            yield objects.Judgement(source=objects.System(), target=person, value=True)
        else:
            yield objects.Judgement(source=objects.System(), target=person, value=False)


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
        Value is True if Quorum exists on respective question.
    """
    number_participants = activity.engagement_in_meeting(meeting)
    return [
        activity.quorum_exists_question(question, number_participants=number_participants,
                                        quorum_threshold=quorum_threshold)
        for question in meeting.questions.data
    ]

