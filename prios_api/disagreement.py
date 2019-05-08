
"""
PRIOS Analytics on Disagreement.
"""

import numpy as np
import pandas as pd
from typing import List, TypeVar, Dict
from prios_api import activity, concepts
from prios_api.concepts import synthesis, polarizing
from prios_api.src import foundation, utils
from prios_api.concepts import disagreement, believable_choice, divisiveness
from prios_api.domain_objects import meta, objects
from statistics import stdev

StringOrFloat = TypeVar("StringOrFloat", str, float)

_THRESHOLD_STD_MAPPED_SCALE = 0.5
_UNIQUE_DISAGREEMENT = 0.88
_THRESHOLD_DICT = {
    'divisiveness': 1.0,
    'mapped_divisiveness': 0.5,
    'polarization': 0.25
}
UNIQUE_RESPONSE = 1
OTHER_RESPONSE = 2


def dots_on_subjects_are_nubby_and_polarizing(dots: List[objects.Dot],
                                              thresholds: Dict[str, float] = _THRESHOLD_DICT) \
                                              ->List[meta.Assertion]:
    """
    Returns list of Assertions for each subject (target) in a list of Dots with a True/False
    value on whether the distribution of author-synthesized dot ratings that they received are
    "polarizing".

    1. Values about a target given by each source is synthesized.
    2. Determines whether the synthesized values have a polarizing distribution. A distribution of
    values is polarizing if the following statistics exceed threshold values
    - its standard deviation (divisiveness)
    - the standard deviation of the values mapped to negative/neutral/positive (semantic
    divisiveness)
    - the ratio and inverse ratio between the numbers of positive opinions (>= 7) and negative
    opinions (<5) (polarization)

    Parameters
    ----------
    dots
    thresholds
        Dictionary containing thresholds at keys for:
        * 'divisiveness': Divisiveness of raw values (Default = 1.0)
        * 'mapped_divisiveness': Divisiveness of values mapped to semantic scale (Default = 0.5)
        * 'polarization': Minimum of ratio between positive to negative opinions and ratio
        between negative to positive opinions (Default = 0.25)

    Returns
    -------
    List[meta.Assertion]
        Target of each Assertion is a subject. Value is True if distribution of dot ratings (
        synthesized by author) is nubby and polarizing .

    Examples
    --------
    >>> adam = objects.Person(name='Adam', uuid='Adam')
    >>> bob = objects.Person(name='Bob', uuid='Bob')
    >>> charlie = objects.Person(name='Charlie', uuid='Charlie')
    >>> dots = list()
    >>> dots.append(objects.Dot(source=adam, target=bob, value=10))
    >>> dots.append(objects.Dot(source=adam, target=bob, value=10))
    >>> result = dots_on_subjects_are_nubby_and_polarizing(dots)
    >>> for x in result:
    ...     print(x.target.name, x.value)
    Bob False
    >>> dots.append(objects.Dot(source=charlie, target=bob, value=1))
    >>> dots.append(objects.Dot(source=charlie, target=bob, value=1))
    >>> dots.append(objects.Dot(source=bob, target=adam, value=10))
    >>> result = dots_on_subjects_are_nubby_and_polarizing(dots)
    >>> for x in result:
    ...     print(x.target.name, x.value)
    Bob True
    Adam False
    >>> dots.append(objects.Dot(source=charlie, target=adam, value=1))
    >>> dots.append(objects.Dot(source=charlie, target=adam, value=1))
    >>> dots.append(objects.Dot(source=bob, target=adam, value=10))
    >>> dots.append(objects.Dot(source=bob, target=adam, value=10))
    >>> result = dots_on_subjects_are_nubby_and_polarizing(dots)
    >>> for x in result:
    ...     print(x.target.name, x.value)
    Bob True
    Adam True
    """
    def key_func(x):
        return x.source.uuid, x.target.uuid

    # Synthesize author opinions of each subject.
    values_grp_by_author_subject = utils.group_assertions_by_key(dots, key_func=key_func)
    subjects = dict()
    for x in values_grp_by_author_subject:
        one_synthesis = synthesis.synthesize([dot.value for dot in x[1]])
        if x[0][1] in subjects.keys():
            subjects[x[0][1]].append(one_synthesis)
        else:
            subjects[x[0][1]] = [one_synthesis]

    uuid_to_person = {
        dot.target.uuid: dot.target for dot in dots
    }

    # Identify subjects whose author syntheses satisfy divisiveness and polarization conditions.
    results = list()
    for sub, values in subjects.items():
        values_divisiveness = divisiveness.divisiveness_stat(values, objects.QuestionType.SCALE,
                                                             map_to_sentiment=False)
        mapped_values_divisiveness = divisiveness.divisiveness_stat(values,
                                                                    objects.QuestionType.SCALE)
        values_polarization = polarizing.polarizing_stat(values)
        is_polarizing = (values_divisiveness > thresholds['divisiveness'] and \
                         mapped_values_divisiveness > thresholds['mapped_divisiveness'] and \
                         values_polarization  > thresholds['polarization'])
        results.append(meta.Assertion(source=objects.System, target=uuid_to_person[sub],
                                      value=is_polarizing))

    return results


def dots_in_meeting_are_polarizing(meeting: objects.Meeting,
                                   by_action: Dict[str, str] = None) -> List[meta.Assertion]:
    """
    Returns Assertion on whether a List of Dots are Polarizing.

    Parameters
    ----------
    meeting
        Meeting object
    by_action
        Specifies mapping from Attribute to Action. Assumes that Attributes and Actions are
        represented as strings.

    Returns
    -------
    List[meta.Assertion]
        Whether or not Dots are polarizing (by action or for entire meeting)
    """
    # TODO: Represent Attributes by objects instead of strings.

    # TODO: Below is all Data Plumbing -- need to define utility function for it.
    dots_df = pd.DataFrame.from_records([(dot.source, dot.target, dot.value) for dot in
                                         meeting.dots], columns=['author', 'subject', 'value'])

    if by_action:
        dots_df['by'] = [by_action[dot.attribute.name] for dot in meeting.dots]
    else:
        dots_df['by'] = "all_dots"

    results = list()
    for action, df in dots_df.groupby(['by']):
        is_polar = disagreement.is_polarizing(list(df['value']))
        results.append(meta.Assertion(source=objects.System, target=objects.Person,
                                      value=is_polar, label=action))
    return results


def dots_on_subject_are_polarizing(dots: List[objects.Dot]) -> List[meta.Assertion]:
    """
    Returns list of Assertions for each subject (target) in a list of Dots with a True/False
    value on whether the distribution of author-synthesized dot ratings that they received are
    polarizing.

    1. Values about a target given by each source is synthesized.
    2. Determines whether the synthesized values have a polarizing distribution.

    TODO: Disentangle into core concepts.

    Parameters
    ----------
    dots

    Returns
    -------
    List[meta.Assertion]
        Target of each Assertion is a topic/subject. Value is True if it is polarizing.
    """
    # TODO: Below is all Data Plumbing -- need to define utility function for it.
    author_subject_value = [
        (dot.source, dot.target, dot.value) for dot in dots
    ]
    author_subject_value_df = pd.DataFrame.from_records(author_subject_value, columns=['author',
                                                                                       'subject',
                                                                                       'value'])
    synthesized_ratings = author_subject_value_df.groupby(['author', 'subject']).apply(concepts.syntheses.synthesize)
    synthesized_ratings = synthesized_ratings.to_frame().reset_index()
    polarizing_subjects = synthesized_ratings.groupby(['subject'])['value'].apply(
        concepts.disagreement.is_polarizing).to_dict()

    results = list()
    for subject, polar in polarizing_subjects.items():
        results.append(meta.Assertion(source=objects.System, target=subject, value=polar))
    return results


def unique_choice(question: objects.Question,
                  unique_disagreement=_UNIQUE_DISAGREEMENT) -> List[meta.Assertion]:
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
    values = [xi.value for xi in question.responses]
    all_buckets = foundation.map_values(values, objects.NumericRange)
    percent = foundation.counts(all_buckets, normalize=True)
    results = list()
    for response in question.responses:
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
                          for response in question.responses]
    value_type = question.question_type

    # Get the Believable choice
    total_believability = sum([x[1] for x in values_and_weights])

    if not total_believability:
        choice = None
    else:
        choice = concepts.believable_choice.believable_choice(values_and_weights, value_type)

    return meta.Assertion(source=objects.System, target=question, value=choice)


def is_nubby_question(question: objects.Question, question_type,
                      threshold: float = _THRESHOLD_STD_MAPPED_SCALE) -> meta.Assertion:
    """
    Is a question Nubby?

    Parameters
    ----------
    question
    question_type
    threshold
        Question is Nubby if its divisiveness value exceeds this quantity.

    Returns
    -------
    meta.Assertion
        Value is True if the question is Nubby.

    Examples
    --------
    >>> from prios_api.examples import binaryexample
    >>> print((is_nubby_question(binaryexample.question, question_type=objects.QuestionType.BINARY)).value)
    False
    >>> from prios_api.examples import likertexample
    >>> print((is_nubby_question(likertexample.question, question_type=objects.QuestionType.LIKERT)).value)
    True
    >>> from prios_api.examples import categoricalexample
    >>> print((is_nubby_question(categoricalexample.question, question_type=objects.QuestionType.CATEGORICAL)).value)
    True
    >>> from prios_api.examples import scaleexample
    >>> print((is_nubby_question(scaleexample.question, question_type=objects.QuestionType.SCALE)).value)
    False
    >>> from prios_api.examples import singleresponseexample
    >>> print((is_nubby_question(singleresponseexample.question, question_type=objects.QuestionType.LIKERT)).value)
    False
    """
    # TODO: Create extractor method in `objects.Question` that returns list of responses?
    values = [response.value for response in question.responses]
    if len(values) < 2:  # TODO: reasonable heuristic... where should it live?
        result = False
    else:
        result = divisiveness.divisiveness_stat(values, value_type=question_type) > threshold
    return meta.Assertion(target=question, value=result)


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
        return [q.response.value for q in nubby_questions.responses]

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


def out_of_sync_people_on_question(question: objects.Question) -> List[meta.Assertion]:
    """
    Identifies people who are out-of-sync on a question.

    TODO: Move logic to prios_api.

    Parameters
    ----------
    question

    Returns
    -------
    List[meta.Assertion]
        Values are True if person is out-of-sync on the question.

    Examples
    --------
    >>> from prios_api.examples import binaryexample
    >>> x = out_of_sync_people_on_question(binaryexample.question)
    >>> for xi in x:
    ...    print(xi.value)
    """
    believable_choice_result = believable_choice_on_question(question)
    disagrees_with_result = disagreement.disagrees_with_167(question)
    people = []
    for response in question.responses:
        result = disagrees_with_result and (believable_choice_result or isinstance(believable_choice_result, float))
        people.append(meta.Assertion(source=objects.System, target=response.source, value=result,
                                     measure=objects.AssertionSet))
    return people


def believable_consensus_exists(question: objects.Question) -> meta.Assertion:
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


def significantly_out_of_sync_in_meeting(meeting: objects.Meeting,
                                         threshold_low=0.8,
                                         threshold_high=1.2) -> List[meta.Assertion]:
    """
    A person is out of sync on significantly higher number of questions than others in a meeting.

    Parameters
    ----------
    meeting
    threshold_low
        A Person is Significantly OOS if they are notable and the Z-score of the number of
        questions on which they were OOS exceeds this quantity.
    threshold_high
        A Person is Significantly OOS if they are not notable and the Z-score of the number of
        questions on which they were OOS exceeds this quantity.

    Returns
    -------
    List[meta.Assertion]
        Value = True if person is Significantly OOS.
    """
    oos = {
        q.id: out_of_sync_people_on_question(q.id) for q in meeting.questions
    }

    oos_count = {
        person: 0 for person in meeting.participants
    }

    for q, is_oos in oos.items():
        for person in is_oos:
            if person.value:
                oos_count[person] += 1

    # TODO: Factor this better.
    oos_count_z_score = foundation.zscore([value for key, value in oos_count.items()])
    oos_count_z_score_dict = dict()
    j = 0
    for key, value in oos_count.items():
        oos_count_z_score_dict[key] = oos_count_z_score[j]
        j += 1

    notable_people = activity.notable_participants(meeting)

    results = []
    for person, v in oos_count_z_score_dict.items():
        for person_notable in notable_people:
            if person.id == person_notable.target.id:
                if person_notable.value:
                    result_person = v > threshold_low
                else:
                    result_person = v > threshold_high

        results += [
            meta.Assertion(source=objects.System, target=person, value=result_person)
        ]
    return results
