
from src import objects, meta
from analytics import foundation


def quality(x: objects.AssertionSet):
    """
    Note:
        * Defines "Meeting Section Quality" as the average of Rankings reflected in Question Responses to "Rate the Section".
        * Returns a Scale Value representing the Meeting Section Quality.
        * Returns Null if there are no "Rate the Section" Questions or Responses.
        * This is produced by the following operation(s):
            * Calculates the average of all Question Responses to "Rate the Section".

    Args:
        dots (objects.AssertionSet): A set of :class:`objects.Dot`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.AssertionSet: A set of relevant actions in a meeting, or an empty set if none exist.
    """
    pass


def sentiment(scale_assertions: objects.ScaleValueSet):
    """
    Defines "Sentiment" as the [Dots Summary](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=186) of all Dots in a Meeting.

    Args:
        scale_assertions (objects.CollectionOfScaleValues): A set of :type:float.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.Assertion: A value representing sentiment, or None.
    """
    result = foundation.weighted_average([i.value for i in scale_assertions.data])
    return meta.Assertion(source=objects.System, target=scale_assertions, value=result)


def importance(x: objects.AssertionSet):
    """
    Note:
        * Classifies Meeting Sections as Critical, Very Important, Important, Typical, or Unremarkable based on the number of Important People in the Meeting Section and the number of generated Dots and Questions.
        * Returns a Statistic between 0-1 that represents the classification of a Meeting Section's Importance.
        * This is produced by the following operation(s):
            * Calculates a Person Importance Value for each Participant based on their General Believability, and if provided, job level and whether they belong to particular Management Groups (job level and membership to management groups are not currently provided in the pilot). Defaults to zero.
            * Calculates the Important People Scaling Factor: calculates how many People had nonzero Person Importance (capped at 4).
            * Calculates the Activity Scaling Factor: calculates a statistic representing how much activity occurred in the Meeting Section based on Dots and Questions and achieves its maximum value at 100 Dots or 10 Questions.
            * Calculates the Dot Scaling Factor, which is a function of how many Dots were given in a Meeting Section and achieves its maximum value at 20 Dots.
            * Calculates the Total Importance: calculates the sum of all Meeting Section Participants' Person Importance.
            * Calculates the overall Meeting Section Importance Value: calculates the product of the Total Importance and the three Scaling Factors above.
            * Determines which classification the Meeting Section Importance Value receives and returns the associated text label (Critical, Very Important, Important, Typical, or Unremarkable).
        * To produce a result at the Meeting level (as opposed to Meeting Section Level), there is code living in the application which labels a Meeting based on the results from this analytic for the first Meeting Section only.

    Args:
        dots (objects.AssertionSet): A set of :class:`objects.Dot`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.AssertionSet: A set of relevant actions in a meeting, or an empty set if none exist.
    """
    pass

