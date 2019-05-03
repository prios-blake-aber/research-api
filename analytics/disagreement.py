
import itertools
import numpy as np
from typing import Tuple, List, TypeVar, Any
from analytics import foundation, utils
from src import objects, meta
from analytics.concepts import believable_choice


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


def polarizing_topics(dots: List[objects.Dot]) -> List[meta.Assertion]:
    """
    Is a "topic" polarizing? A topic is a collection of Assertions on a single target.

    1. Values about a target given by each source is synthesized.
    2. Determines whether the synthesized values have a polarizing distribution.
    TODO: Generalize input type beyond Dots.
    TODO: Disentangle into core concepts.

    Parameters
    ----------
    dots

    Returns
    -------
    List[meta.Assertion]
        Target of each Assertion is a topic/subject. Value is True if it is polarizing.
    """
    syntheses = synthesize(dots)
    targets = set([s.target for s in syntheses])
    result = []
    for t in targets:
        target_syntheses = [s for s in syntheses if s.target == t]
        target_is_polarizing = is_polarizing(target_syntheses)
        target_is_polarizing.target = t
        result += [target_is_polarizing]
    return result


def synthesize(dots: List[objects.Dot]) -> List[meta.Assertion]:
    """
    Synthesize dots given by each author (source) about a single subject (target) into a single
    assertion.
    TODO: Synthesis is a core concept.
    TODO: Add keyword arguments for specifying how syntheses are performed

    Parameters
    ----------
    dots

    Returns
    -------
    List[meta.Assertion]

    """
    sources = set([dot.source for dot in dots])
    targets = set([dot.target for dot in dots])

    result = list()
    for s in sources:
        for t in targets:
            subset_dots = [dot for dot in dots if dot.source == s and dot.target == t]
            values = [dot.value for dot in subset_dots]
            synthesized_value = foundation.weighted_average(values)
            result.append(
                meta.Assertion(
                    source=s,
                    target=t,
                    value=synthesized_value
                )
            )
    return result


def disagrees_with_167(values : Tuple[Any, Any], question_type) -> meta.Assertion:
    """

    TODO: other analytics that use disagrees_with are Out of Sync People, Uniquely Out of Sync,
    Significantly OOS, etc.

    Parameters
    ----------
    values

    Returns
    -------
    objects.AssertionSet
        Empty set, if none exists.
    """
    response, response_value = values
    categorical_binary = question_type in (objects.QuestionType.CATEGORICAL, objects.QuestionType.BINARY)
    numeric = question_type in (objects.QuestionType.LIKERT, objects.QuestionType.SCALE)

    if categorical_binary:
        return disagrees_with_categorical_binary(response, response_value)
    elif numeric:
        return disagrees_with_numeric(response, response_value)
    else:
        return None


def disagrees_with_categorical_binary(response_to_compare: StringOrFloat,
                                      answer_to_compare: StringOrFloat) -> meta.Assertion:
    """
    Disagrees With logic for Categorical/Binary values.

    TODO: Find better home -> is this a core concept?

    Parameters
    ----------
    response_to_compare
    answer_to_compare

    Returns
    -------
    meta.Assertion
        Value is True, if there is a disagreement.
    """
    result = response_to_compare != answer_to_compare
    return meta.Assertion(source=objects.System, target=response_to_compare, value=result,
                          measure=objects.BooleanOption)


def disagrees_with_numeric(response_to_compare: float,
                           answer_to_compare: float,
                           far_away: float=_THRESHOLD_HIGH) -> meta.Assertion:
    """
    Disagrees With logic for Scale values (1-to-10 or 1-to-5).

    TODO: Find better home -> is this a core concept?

    Parameters
    ----------
    response_to_compare
    answer_to_compare

    Returns
    -------
    meta.Assertion
        Value is True, if there is a disagreement.
    """
    buckets = foundation.map_values([response_to_compare, answer_to_compare], objects.NumericRange)
    same_bucket = buckets[0] == buckets[1]

    try:
        far_away = abs(response_to_compare - answer_to_compare) > far_away

        result = far_away and not same_bucket
        return meta.Assertion(source=objects.System, target=response_to_compare, value=result,
                              measure=objects.FloatOption)

    except TypeError:
        return not same_bucket


def is_unique(question: objects.Question, unique_disagreement=_UNIQUE_DISAGREEMENT) -> List[
    meta.Assertion]:
    """
    Determines whether responses are in small minority of responses.

    TODO: bucketing should live in it's own function
    Identify if the given 'response' is unique in relation to the given set of 'responses'.


    Parameters
    ----------
    question
    unique_disagreement
        Response is unique if its percentage (compared to all responses) is less than this value

    Returns
    -------
    List[meta.Assertion]
        System assertions of whether each response is unique
    """
    values = [xi.value for xi in question.responses.data]
    all_buckets = foundation.map_values(values, objects.NumericRange)
    percent = foundation.counts(all_buckets, normalize=True)
    results = list()
    for response in question.responses.data:
        if percent[response.value] < unique_disagreement:
            unique = True
        else:
            unique = False
        results.append(meta.Assertion(source=objects.System, target=response.source, value=unique))
    return results


def believable_choice_on_question(question: objects.Question) -> meta.Assertion:
    """
    What is the believable choice on a question?

    Parameters
    ----------
    question

    Returns
    -------
    meta.Assertion
        Value
    """

    # Extract responses and question data.
    values_and_weights = [(response.value, response.source.believability)
                          for response in question.responses.data]
    value_type = question.question_type

    # Get the Believable choice
    choice = believable_choice(values_and_weights, value_type)

    return meta.Assertion(
        source=objects.System,
        target=question,
        value=choice
    )


def is_nubby_question(question: objects.Question,
                      threshold: float = _THRESHOLD_STD_MAPPED_SCALE) -> meta.Assertion:
    """
    Is a question Nubby?

    Parameters
    ----------
    question
    threshold
        Question is Nubby if its divisiveness value exceeds this quantity.

    Returns
    -------
    meta.Assertion
        Value is True if the question is Nubby.
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
    """
    Is a Meeting Nubby?

    TODO: Public.
    TODO: Default Thresholds are wrong.

    Parameters
    ----------
    meeting
    thresholds

    Returns
    -------
    meta.Assertion
        Value is a Classification.
    """
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


def divisiveness(ar: List[StringOrFloat], value_type: objects.QuestionType) -> float:
    """
    Divisiveness.

    # TODO: Core Concept.
    # TODO: How are N/A's being represented? We shouldn't assume they're being filtered.

    Parameters
    ----------
    ar
    value_type

    Returns
    -------
    float
        Divisiveness value
    """
    if value_type in [objects.QuestionType.SCALE, objects.QuestionType.LIKERT]:
        return foundation.standard_deviation(ar)
    elif value_type == objects.QuestionType.CATEGORICAL:
        count = [v for k, v in foundation.counts(ar).items()]
        max_count = max(count)
        mapped_ar = [0]*max_count + [1]*(len(ar) - max_count)
        return foundation.standard_deviation(mapped_ar)


def out_of_sync_people_on_question(question: objects.Question) -> List[meta.Assertion]:
    """
    Identifies people who are out-of-sync on a question.

    TODO: Move logic to analytics.

    Parameters
    ----------
    question

    Returns
    -------
    List[meta.Assertion]
        Values are True if person is out-of-sync on the question.
    """
    believable_choice_result = believable_choice_on_question(question)
    disagrees_with_result = disagrees_with_167(question)
    people = []
    for response in question.responses.data:
        result = disagrees_with_result and (believable_choice_result or isinstance(believable_choice_result, float))
        people.append(meta.Assertion(source=objects.System, target=response.source, value=result,
                                     measure=objects.AssertionSet))
    return people


