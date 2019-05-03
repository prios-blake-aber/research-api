
import itertools
import numpy as np
from typing import Tuple, List, TypeVar, Any
from analytics import foundation, utils
from src import objects, meta


StringOrFloat = TypeVar("StringOrFloat", str, float)

_THRESHOLD_HIGH = 1.7
_THRESHOLD_STD_SCALE = 1.0
_THRESHOLD_STD_MAPPED_SCALE = 0.5
_THRESHOLD_POLES = 0.25
_UNIQUE_DISAGREEMENT = 0.88

"""
Core functionality for Disagreement
"""


def substantive_disagreement(scale_values: Tuple[float, float],
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
    scale_values
        Scale Value Pair
    threshold_high
        Returns False if difference between raw values is less than this quantity.

    Returns
    -------
    object.Judgement
        Whether there's substantive disagreement between two assertions.
    """
    x1, x2 = scale_values
    diff = abs(x1.value - x2.value)
    far_away = diff > threshold_high
    mapped_x1 = foundation.map_values(x1.value, objects.NumericRange.ONE_TO_TEN)
    mapped_x2 = foundation.map_values(x2.value, objects.NumericRange.ONE_TO_TEN)
    mapped_diff = abs(mapped_x1 - mapped_x2)
    result = far_away and mapped_diff
    return result


def is_polarizing(scale_assertions: objects.ScaleValueSet,
                  thresh_on_std_scale: float = _THRESHOLD_STD_SCALE,
                  thresh_on_std_mapped_scale: float = _THRESHOLD_STD_MAPPED_SCALE,
                  thresh_on_poles: float = _THRESHOLD_POLES) -> objects.Judgement:

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
    values = [xi.value for xi in scale_assertions.data]
    mapped_values = [foundation.map_values(vi, objects.NumericRange.ONE_TO_TEN) for vi in values]

    # TODO: nesting functions here is terrible; why not use the sentiment module?
    def negative_sentiment(x):
        return x == 1

    def positive_sentiment(x):
        return x == 3

    percent_negative = foundation.percent_satisfying_condition(mapped_values, negative_sentiment)
    percent_positive = foundation.percent_satisfying_condition(mapped_values, positive_sentiment)

    if percent_negative > 0 and percent_positive > 0:
        pole_ratio = min(percent_positive/percent_negative, percent_negative/percent_positive)
    else:
        pole_ratio = 0

    std_values_condition = foundation.standard_deviation(values) > thresh_on_std_scale
    std_mapped_values_condition = foundation.standard_deviation(mapped_values) > thresh_on_std_mapped_scale
    pole_condition = pole_ratio > thresh_on_poles
    result = std_values_condition and std_mapped_values_condition and pole_condition
    return objects.Judgement(source=objects.System, target=objects.System, value=result)


def polarizing_topics(dots: List[objects.Dot]) -> List[objects.Judgement]:
    """
    TODO: Generalize input type beyond Dots.

    Parameters
    ----------
    dots

    Returns
    -------
    List[objects.Judgement]
    """
    target = set([dot.target for dot in dots])
    result = []
    for s in target:
        target_dots = [dot for dot in dots if dot.source == s]
        author_syntheses = syntheses(target_dots)
        subject_is_polarizing = is_polarizing(author_syntheses)
        subject_is_polarizing.target = s
        result += [subject_is_polarizing]
    return result


def syntheses(dots: List[objects.Dot]) -> List[meta.Assertion]:
    """
    TODO: Synthesize Ratings in a list of Assertions by Source.
    TODO: Find a better home for this.
    TODO: Add keyword arguments for specifying how syntheses are performed
    TODO: Potentially as a utility function

    Parameters
    ----------
    dots

    Returns
    -------
    List[meta.Assertion]
    """
    pass


def disagrees_with_167(question: objects.Question):
    """
    TODO: other analytics that use disagrees_with are Out of Sync People, Uniquely Out of Sync, Significantly OOS, etc.
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
    categorical_binary = ('CATEGORICAL' in objects.QuestionType.__members__.keys()) | (
            'BINARY' in objects.QuestionType.__members__.keys())
    numeric = ('LIKERT' in objects.QuestionType.__members__.keys()) | (
            'SCALE' in objects.QuestionType.__members__.keys())

    answer_to_compare = believable_choice(question)

    for response in question.responses.data:
        response_to_compare = response
        if response_to_compare is None or answer_to_compare is None:
            return False
        elif categorical_binary:
            return disagrees_with_categorical_binary(response_to_compare, answer_to_compare)
        elif numeric:
            return disagrees_with_numeric(response_to_compare, answer_to_compare)
        else:
            return None


def disagrees_with_categorical_binary(response_to_compare, answer_to_compare):
    result = response_to_compare != answer_to_compare
    return meta.Assertion(source=objects.System, target=response_to_compare, value=result,
                          measure=objects.BooleanOption)


def disagrees_with_numeric(response_to_compare, answer_to_compare, far_away=_THRESHOLD_HIGH):
    buckets = foundation.map_values([response_to_compare, answer_to_compare], objects.NumericRange)
    same_bucket = buckets[0] == buckets[1]

    try:
        far_away = abs(response_to_compare - answer_to_compare) > far_away

        result = far_away and not same_bucket
        return meta.Assertion(source=objects.System, target=response_to_compare, value=result, measure=objects.FloatOption)

    except TypeError:
        return not same_bucket


def is_unique(question: objects.Question, unique_disagreement=_UNIQUE_DISAGREEMENT):
    """Identify if the given 'response' is unique in relation to the given set of 'responses'.

        Parameters
        ----------
        response
            The specific response that is being tested as unique or not. This should be
            of the same type as elements of 'responses', though a discrepancy will not necessarily
            trigger an exception.

        responses : iterable of responses of any type
            An iterable of responses, corresponding to the `response_type`.

        response_type : :class:`ResponseType`
            The type of each element of `responses`. This must be one of the elements of the
            ResponseType enum. This will govern how responses are bucketed.

        Returns
        -------
        bool
            True if `response` is unique among `responses`. False otherwise.  Uniqueness is
            defined as 88% of other responses being in a different response 'bucket'.
        """
    values = [xi.value for xi in question.responses.data]
    all_buckets = [foundation.map_values(vi, objects.NumericRange) for vi in values]
    assertions = []
    for value in all_buckets:
        count_responses_in_diff_bucket = 0
        if all_buckets[1:] != all_buckets[0]:
            count_responses_in_diff_bucket += 1
        pct_bucket_disagree = count_responses_in_diff_bucket / len(values)
        result = pct_bucket_disagree > unique_disagreement
        assertions.append(meta.Assertion(source=objects.System, target=values, value=result, measure=objects.BooleanOption))
    return assertions



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

    if not total_believability:
        return None
    elif categorical_binary:
        return believable_choice_categorical_binary(question, total_believability)
    elif numeric:
        return believable_choice_numeric(question, total_believability)
    else:
        return None


def believable_choice_numeric(question: objects.Question):
    values = [response.value for response in question.responses.data]
    weights = [response.source.believability for response in question.responses.data]
    result = foundation.weighted_average(values, weights)
    return meta.Assertion(source=objects.System, target=question, value=result, measure=objects.FloatOption)


def believable_choice_categorical_binary(question: objects.Question, total_believability=None):
    sorted_responses = sorted(question.responses.data, key=lambda x: x.value)
    for response_choice, response_set in itertools.groupby(sorted_responses, key=lambda x: x.value):
        if sum([i.source.believability for i in response_set]) / total_believability > 0.7:
            result = response_choice
    return meta.Assertion(source=objects.System, target=question, value=result, measure=objects.BooleanOption)


def is_nubby_question(question: objects.Question,
                      threshold: float = _THRESHOLD_STD_MAPPED_SCALE) -> meta.Assertion:
    """
    Is a question Nubby?

    Parameters
    ----------
    question

    Returns
    -------
    meta.Assertion
    """
    # TODO: Create extractor method in `objects.Question` that returns list of responses?
    values = [response.value for response in question.responses.data]
    if len(values) < 2:
        result = False
    else:
        mapped_values = foundation.map_values(values)
        result = divisiveness(mapped_values, question.question_type) > threshold

    return meta.Assertion(source=objects.System, target=question, value=result,
                          measure=objects.BooleanOption)


def meeting_nubbiness_v1(meeting: objects.Meeting,
                         thresholds: List[float] = [0.2, 0.4, 0.6, 0.8]) -> meta.Assertion:
    # TODO: Public.
    # TODO: Default Thresholds are wrong.
    nubby_questions = [q for q in meeting.questions if is_nubby_question(q)]

    def responses_to_list(question):
        return [q.response.value for q in nubby_questions.responses.data]

    if len(nubby_questions) == 0:
        meeting_divisiveness = 0.0
    else:
        meeting_divisiveness = [
            divisiveness(responses_to_list(q)) for q in nubby_questions
        ]

    scaling_factor = 0.5 if len(nubby_questions) == 1 else 0

    meeting_nubbiness = scaling_factor * meeting_divisiveness

    # TODO: Generalize classification object.
    # TODO: Add "classify" to Core Concepts.
    classification = objects.MeetingNubbyClassification(np.digitize(meeting_nubbiness, thresholds))
    return meta.Assertion(
        source=objects.System,
        target= meeting.id,
        value=classification,
        measure=objects.MeetingNubbyClassification
    )


def divisiveness(ar: List[StringOrFloat], value_type: objects.QuestionType):
    # TODO: Core Concept.
    # TODO: How are N/A's being represented? We shouldn't assume they're being filtered.
    if value_type in [objects.QuestionType.SCALE, objects.QuestionType.LIKERT]:
        return foundation.standard_deviation(ar)
    elif value_type == objects.QuestionType.CATEGORICAL:
        count = [v for k, v in foundation.counts(ar).items()]
        max_count = max(count)
        mapped_ar = [0]*max_count + [1]*(len(ar) - max_count)
        return foundation.standard_deviation(mapped_ar)
