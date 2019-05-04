
"""
TBD
"""

from src import objects, meta
from analytics import foundation


def quality(x: objects.AssertionSet):
    """
    Args:
        dots (objects.AssertionSet): A set of :class:`objects.Dot`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.AssertionSet: A set of relevant actions in a meeting, or an empty set if none exist.
    """
    pass


def sentiment(scale_assertions: objects.ScaleValueSet, **kwargs):
    """
    Defines "Sentiment" as the [Dots Summary](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=186) of all Dots in a Meeting.

    Args:
        scale_assertions (objects.CollectionOfScaleValues): A set of :type:float.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.Assertion: A value representing sentiment, or None.
    """
    result = foundation.weighted_average([i.value for i in scale_assertions.data], **kwargs)
    return meta.Assertion(source=objects.System, target=scale_assertions, value=result)
