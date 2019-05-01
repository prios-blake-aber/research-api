
import itertools
import numpy as np
from analytics import utils
from src import objects, meta
from analytics.foundation import map_values, percent_satisfying_condition, standard_deviation
from src.objects import NumericRange
_THRESHOLD_HIGH = 1.7
_THRESHOLD_STD_SCALE = 1.0
_THRESHOLD_STD_MAPPED_SCALE = 0.5
_THRESHOLD_POLES = 0.25

"""
Core functionality for Disagreement
"""


def substantive_disagreement(x1: meta.Assertion, x2: meta.Assertion,
                             threshold_high: float = _THRESHOLD_HIGH):
    """
    Substantive disagreement

    * Identifies a pair of Scale Values that Substantively Disagree.
    * Returns a Boolean representing whether Substantive Disagreement exists.
    * This is produced by the following operation(s):
        * Calculates the absolute difference between the two values.
        * Determines whether the values are Far Away: Compares whether the difference is greater
        than a threshold of 1.7.
        * Maps Responses into Summarized Opinions.
        * Determines whether the Summarized Opinions Disagree: determines whether their values are
        different.
        * Returns True if both of the above conditions are True.

    Parameters
    ----------
    x1
        Assertion 1
    x2
        Assertion 2
    threshold_high
        Returns False if difference between raw values is less than this quantity.

    Returns
    -------
    object.Judgement
        Whether there's substantive disagreement between two assertions.
    """
    diff = abs(x1.value - x2.value)
    far_away = diff > threshold_high
    mapped_x1 = map_values(x1.value, NumericRange.ONE_TO_TEN)
    mapped_x2 = map_values(x2.value, NumericRange.ONE_TO_TEN)
    mapped_diff = abs(mapped_x1 - mapped_x2)
    result = far_away and mapped_diff
    return objects.Judgement(source=x1.source, target=x2.source, value=result)


def is_polarizing(scale_assertions: objects.CollectionOfScaleValues,
                  thresh_on_std_scale: float = _THRESHOLD_STD_SCALE,
                  thresh_on_std_mapped_scale: float = _THRESHOLD_STD_MAPPED_SCALE,
                  thresh_on_poles: float = _THRESHOLD_POLES) -> object.Judgement:
    """
    Is Polarizing

    From Key Points
    * Identifies a Polarizing event when Scale Values on a Person are spread out and there exist
    comparable numbers of positive (8 and above) and negative (4 and below) Scale Values
    * Returns a boolean
    * This is produced by the following operation(s):
        * Calculates the standard deviation of Scale Values
        * Calculates the Bucketed Standard Deviation of Scale Values:
            * Maps the Scale Values to their Summarized Opinion
            * Calculates the standard deviation
        * Calculates the Relative Incidence Ratio of positive/negative Scale Values
            * Calculates the numerator as the minimum count of positive/negative Scale Values
            * Calculates the Denominator as the maximum count of positive/negative Scale Values
        * Combines the following conditions to determine whether the Scale Values are polarizing:
            * Calculates the standard deviation of Scale Values is greater than 0.5
            * Calculates the Bucketed Standard Deviation of Scale Values is greater than 1.0
            * Calculates the Relative Incidence Ratio of positive/negative Scale Values is greater
            than 0.25

    Parameters
    ----------
    scale_assertions
        List of assertions with scale values.
    thresh_on_std_scale
        Threshold on standard deviation of scale values.
    thresh_on_std_mapped_scale
        Threshold on standard deviation of scale values mapped to 1, 2, and 3
    thresh_on_poles
        Threshold on ratio between poles

    Returns
    -------
    object.Judgement
        Whether a set of scale values are polarizing.
    """
    values = [xi.value for xi in scale_assertions.expected_collections]
    mapped_values = [map_values(vi, NumericRange.ONE_TO_TEN) for vi in values]

    def negative_sentiment(x):
        return x == 1

    def positive_sentiment(x):
        return x == 3

    percent_negative = percent_satisfying_condition(mapped_values, negative_sentiment)
    percent_positive = percent_satisfying_condition(mapped_values, positive_sentiment)

    if percent_negative > 0 and percent_positive > 0:
        pole_ratio = min(percent_positive/percent_negative, percent_negative/percent_positive)
    else:
        pole_ratio = 0

    std_values_condition = standard_deviation(values) > thresh_on_std_scale
    std_mapped_values_condition = standard_deviation(mapped_values) > thresh_on_std_mapped_scale
    pole_condition = pole_ratio > thresh_on_poles
    result = std_values_condition and std_mapped_values_condition and pole_condition
    return objects.Judgement(source=objects.System, target=objects.System, value=result)


def disagrees_with(questions: objects.AssertionSet):
    """
    Note:
        * Defines "Disagreement" between two opinions on a Question. Two opinions disagree when they are classified into different [groups](https://blakea-analytics-registry.dev.principled.io/detail?analytic=168) and, if they are Question Responses with Likert or Scale Values, also have a difference greater than a configurable threshold (with a default value of 1.7).
        * Returns a Boolean representing whether two opinions Disagrees With one another.
        * This is produced by the following operation(s):
            * Determines whether two opinions disagree as:
                * For Categorical or Yes/No opinions: the two opinions are different.
                * For Likert or Scale Value opinions:
                    * Determines whether the two opinions are Far Away: Compares whether the difference is greater than a configurable threshold value (default value of 1.7).
                    * Maps each opinion to a Summarized Opinions (Negative, Neutral, or Positive).
                    * Determines whether the Summarized Opinions Disagree: Determines whether their values are different.
                    * Determines whether the two opinions are Far Away and their Summarized Opinions Disagree.

    Args:
        dots (objects.AssertionSet): A set of :class:`objects.Assertion`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.AssertionSet: A set of relevant :class:`objects.Assertion` in a :class:`objects.Context`, or an empty set if none exist.
    """
    pass


def divisiveness(questions: objects.AssertionSet):
    """
    Note:
        * Defines Divisiveness as the standard deviation of Summarized Opinions reflected in Meeting Question responses.
        * Returns a Statistic representing Divisiveness.
        * Returns Null in the following cases:
            * Fewer than two People respond to a Question.
            * The Question has Categorical Responses.
        * This is produced by the following operation(s):
            * Maps opinions to [Summarized Opinions](https://blakea-analytics-registry.dev.principled.io/detail?analytic=168).
            * Calculates the standard deviation of the Summarized Opinions.

    Args:
        dots (objects.AssertionSet): A set of :class:`objects.Assertion`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.AssertionSet: A set of relevant :class:`objects.Assertion` in a :class:`objects.Context`, or an empty set if none exist.
    """
    pass


def believable_choice(question: objects.Question):
    """
    TK
    """
    total_believability = sum([response.source.believability for response in question.responses.data])
    # TODO: Terrible factorization using QuestionType
    categorical_binary = ('CATEGORICAL' in objects.QuestionType.__members__.keys()) | (
            'BINARY' in objects.QuestionType.__members__.keys())
    numeric = ('LIKERT' in objects.QuestionType.__members__.keys()) | (
            'SCALE' in objects.QuestionType.__members__.keys())

    if categorical_binary:
        return utils.believable_choice_categorical_binary(question, total_believability)
    elif numeric:
        return utils.believable_choice_numeric(question, total_believability)
    else:
        return None






