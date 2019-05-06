"""
Engagement
"""

from typing import List, Any


def engagement(values: List[Any]):
    return len(values)


def quorum_exists(values: List[Any], number_participants, quorum_threshold) -> bool:
    """
    TODO: generalize the concept of minimum_engagement
    Whether a quorum exists within a set of meta.objects.Judgements

    Parameters
    ----------
    values: any meta.objects.Judgements
    number_participants:
    quorum_threshold: The threshold above which quorum exists. Defaults to :data:`_QUORUM_THRESH_DEFAULT`

    Returns
    -------
    bool
        Whether a quorum exists within the set of values.
    """
    if number_participants:
        engagement_on = engagement(values)
        quorum_flag = (engagement_on / number_participants > quorum_threshold) and (engagement_on > 3)
        return quorum_flag
    else:
        return None

