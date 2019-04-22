
from src import objects

"""
Core functionality for Disagreement
"""


def is_polarizing_141(x: objects.AssertionSet):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Disagreement
    PROCESSING: Context-Only

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
    """
    pass


def disagrees_with_167(x: objects.Question):
    """
    OUTPUT: Response
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Comparing [Collections of People]

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
    """
    pass


def divisiveness_179(x: objects.Question):
    """
    OUTPUT: Response
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Defines Divisiveness as the standard deviation of Summarized Opinions reflected in Meeting Question responses.
    * Returns a Statistic representing Divisiveness.
    * Returns Null in the following cases:
        * Fewer than two People respond to a Question.
        * The Question has Categorical Responses.
    * This is produced by the following operation(s):
        * Maps opinions to [Summarized Opinions](https://blakea-analytics-registry.dev.principled.io/detail?analytic=168).
        * Calculates the standard deviation of the Summarized Opinions.
    """
    pass
