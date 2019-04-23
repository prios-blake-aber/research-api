
import itertools
from src import objects
from analytics import utils, activity

"""
Insights on Activities
"""

@utils.select_dots_from_meeting
def actions_in_meeting_156(dots: objects.DotCollection):
    """
    ```DEPRECATED``` The domain model provides this functionality for free.
    """
    pass


@utils.select_dots_from_meeting
def primary_actions_157(dots: objects.DotCollection):
    """
    Defines Primary Actions in a Meeting based on :class:`objects.DotCollection`

    Args:
        dots (objects.DotCollection): A set of :class:`objects.Dot`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.RelevanceCollection: A set of :class:`objects.RelevanceScore`, or an empty set if none exist.
    """
    relevant_actions = action_relevance_158(dots)
    return sorted(relevant_actions, key=lambda x: x.value)[:3]  # top 3 scores


@utils.select_dots_from_meeting
def primary_participants_in_meeting_138(dots: objects.DotCollection):
    """
    Defines Primary Participants in a Meeting based on :class:`objects.DotCollection`

    Args:
        dots (objects.DotCollection): A set of :class:`objects.Dot`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.RelevanceCollection: A set of :class:`objects.RelevanceScore`, or an empty set if none exist.
    """
    total_participation = len(dots)
    dots.sort(key=lambda x: x.source.name, reverse=False)
    for person, dots in itertools.groupby(dots, lambda x: x.target):
        person_dots = len(list(dots))
        if ((person_dots / total_participation) > 0.2) or (person_dots > 10 and ((person_dots / total_participation) > 0.1)):
            yield objects.Judgement(source=objects.System(), target=person, value=True)
        else:
            yield objects.Judgement(source=objects.System(), target=person, value=False)


@utils.select_dots_from_meeting
def action_relevance_158(dots: objects.DotCollection):
    """
    Defines Action Relevance in a Meeting based on :class:`objects.DotCollection`

    Args:
        dots (objects.DotCollection): A set of :class:`objects.Dot`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.RelevanceCollection: A set of :class:`objects.RelevanceScore`, or an empty set if none exist.
    """
    return activity.relevance_of_dots(dots)


@utils.select_dots_from_meeting
def attention_participant_received_155(dots: objects.DotCollection):
    """
    Defines Relevance People in a Meeting based on :class:`objects.DotCollection`

    Args:
        dots (objects.DotCollection): A set of :class:`objects.Dot`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.RelevanceCollection: A set of :class:`objects.RelevanceScore`, or an empty set if none exist.
    """
    return activity.relevance_of_people(dots)
