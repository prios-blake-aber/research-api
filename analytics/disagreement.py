
import itertools
import numpy as np
from src import objects, meta
from analytics import utils

"""
Core functionality for Disagreement
"""


def is_polarizing(x: objects.AssertionSet):
    """
    Note:
        * Identifies a Polarizing event when Scale Values on a Person are spread out and there exist comparable numbers of positive (8 and above) and negative (4 and below) Scale Values
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
                * Calculates the Relative Incidence Ratio of positive/negative Scale Values is greater than 0.25

    Args:
        dots (objects.AssertionSet): A set of :class:`objects.Assertion`.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        objects.AssertionSet: A set of relevant :class:`objects.Assertion` in a :class:`objects.Context`, or an empty set if none exist.
    """
    pass


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
    INSERT DOCSTRING
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






