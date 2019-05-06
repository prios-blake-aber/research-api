
"""
TBD
"""

import itertools
import numpy as np
from typing import Tuple, List, TypeVar, Any
from analytics import foundation, activity, utils
from analytics.concepts import disagreement
from src import objects, meta


StringOrFloat = TypeVar("StringOrFloat", str, float)

_THRESHOLD_STD_MAPPED_SCALE = 0.5
_UNIQUE_DISAGREEMENT = 0.88


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
        target_is_polarizing = disagreement.is_polarizing(target_syntheses)
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
        Value represents the believable choice answer on the question.
    """

    # Extract responses and question data.
    values_and_weights = [(response.value, response.source.believability)
                          for response in question.responses.data]
    value_type = question.question_type

    # Get the Believable choice
    choice = disagreement.believable_choice(values_and_weights, value_type)

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
    disagrees_with_result = disagreement.disagrees_with_167(question)
    people = []
    for response in question.responses.data:
        result = disagrees_with_result and (believable_choice_result or isinstance(believable_choice_result, float))
        people.append(meta.Assertion(source=objects.System, target=response.source, value=result,
                                     measure=objects.AssertionSet))
    return people


def believable_consensus_exists(question: objects.Question) -> objects.meta.Assertion:
    """
    TODO: Needs clarification on where it lives conceptually, what the I/O types should be, whether it can be refactored
    Consensus exists on a question.

    Parameters
    ----------
    question

    Returns
    -------
    bool
        Whether there is a consensus answer.
    """
    sufficient_engagement_flag = activity.quorum_exists_on_question_145(question)
    sufficient_believability_engagement_flag = activity.sufficient_believability_engagement(question)
    believable_choice_results = believable_choice_on_question(question) or isinstance(
        believable_choice_on_question(question), float)
    if sufficient_engagement_flag and sufficient_believability_engagement_flag and believable_choice_results:
        results = True
        return meta.Assertion(source=objects.System, target=question, value=results, measure=objects.BooleanOption)
    else:
        results = False
        return meta.Assertion(source=objects.System, target=question, value=results, measure=objects.BooleanOption)
