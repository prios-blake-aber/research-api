
"""
TBD
"""

import itertools
from src import objects
from analytics import utils, activity


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
