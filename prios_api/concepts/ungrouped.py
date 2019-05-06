
"""
TBD
"""

from prios_api.domain_objects import objects
from typing import List


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


def relevance(dots: objects.AssertionSet):
    pass


def importance(x: objects.AssertionSet):
    pass
