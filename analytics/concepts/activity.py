
"""
TBD
"""

from src import objects, meta
from typing import List, Any



def engagement(values: List[Any]):
    return len(values)


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


def quorum_exists(values: List[Any], number_participants, quorum_threshold):
    if number_participants:
        engagement_on = engagement(values)
        quorum_flag = (engagement_on / number_participants > quorum_threshold) and (engagement_on > 3)
        return quorum_flag
    else:
        return None

