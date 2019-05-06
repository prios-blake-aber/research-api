
"""
TBD
"""

import itertools
from typing import List, Dict
from src import objects, meta
from analytics import utils, disagreement, activity


_QUORUM_THRESH_DEFAULT = 0.80


def believable_choice_130(question: objects.QuestionType) -> meta.Assertion:
    """
    Believable choice.

    Parameters
    ----------
    question

    Returns
    -------
    meta.Assertion
        A single assertion on whether there is a Believable Choice answer to the question and which answer choice it is.
    """
    return disagreement.believable_choice_on_question(question)


@utils.scope_required_data_within_object(collections_to_keep=['dots'])
def action_is_polarizing_161(meeting: objects.Meeting):
    """
    Identifies Meeting Tracker Actions in a Meeting that are polarizing.

    TODO: Reconcile with:
    insights.interaction.believable_view_disagrees_with_overall_view_on_action_162

    Parameters
    ----------
    meeting

    Returns
    -------
    List[objects.Judgement]
        List of Assertions on whether Action is Polarizing.
    """
    def sort_by_measure(x):
        return x.measure.name

    results = []
    dots_by_attribute = sorted(meeting.dots.data, key=sort_by_measure)
    for attribute, dot_set in itertools.groupby(dots_by_attribute, key=sort_by_measure):
        materialized_dot_set = meta.EntityCollection(list(dot_set))
        # TODO: materialization and instantiation is shitty here
        result = disagreement.is_polarizing(materialized_dot_set)
        results.append(result)

    return results


@utils.scope_required_data_within_object(collections_to_keep=['dots'])
def meeting_section_sentiment_is_polarizing_118(meeting: objects.Meeting) -> meta.Assertion:
    """
    Determines if Meeting Section Sentiment is polarizing, based on Dots.

    Parameters
    ----------
    meeting
        Meeting object

    Returns
    -------
    meta.Assertion
    """
    return disagreement.dots_in_meeting_are_polarizing(meeting)


def consensus_exists_131(question: objects.Question) -> bool:
    """
    Consensus exists on a question.

    TODO: Logic is core-functionality. It is also used by a Sig Gen, for the case of questions.

    Parameters
    ----------
    question

    Returns
    -------
    bool
        Whether there is a consensus answer.
    """
    if (activity.sufficient_question_engagement(question)) and (disagreement.believable_choice_on_question(question) is True or float):
        return True
    else:
        return False


def meeting_section_nubbiness_149(meeting: objects.Meeting) -> meta.Assertion:
    """
    Classifies Nubbiness level of a Meeting Section.

    Parameters
    ----------
    meeting

    Returns
    -------
    meta.Assertion
    """
    return disagreement.meeting_nubbiness_v1(meeting)


@utils.scope_required_data_within_object(collections_to_keep=['dots'])
def polarizing_participants_38(meeting: objects.Meeting) -> List[meta.Assertion]:
    """
    People who are polarizing, based on their dots.

    Parameters
    ----------
    meeting

    Returns
    -------
    List[meta.Assertion]
    """
    frequently_dotted = activity.frequently_dotted_subjects(meeting.dots)
    polarizing = disagreement.dots_are_polarizing(meeting.dots)

    # TODO: Write function for determining whether values are True in two (or more) lists of
    #  Judgements. Elements of each list should have the same targets, which only appear once.

    frequently_dotted_dict = {
        person.target.id: person.value for person in frequently_dotted
    }

    polarizing_dict = {
        person.target.id: person.value for person in polarizing
    }

    result = []
    for person, value in polarizing_dict.items():
        is_frequently_dotted = frequently_dotted_dict[person]
        if value and is_frequently_dotted:
            person_is_polarizing = True
        else:
            person_is_polarizing = False
        result.append(
            meta.Assertion(source=objects.System,
                           target=person,
                           value=person_is_polarizing)
        )

    return result


def nubby_question_147(question: objects.Question) -> meta.Assertion:
    """
    Is a Question Nubby?

    Parameters
    ----------
    question

    Returns
    -------
    meta.Assertion
        Value is True if the Question is Nubby.
    """
    return disagreement.is_nubby_question(question)


def question_nubbiness_popup_49(question: objects.Question) -> meta.Assertion:
    """
    Returns True if question is nubby and a quorum exists.

    Parameters
    ----------
    question

    Returns
    -------
    meta.Assertion
        Value is True if the Question is Nubby.
    """
    nubby = disagreement.is_nubby_question(question)
    quorum = activity.quorum_exists_on_question_145(question)
    return meta.Assertion(
        source=objects.System,
        target=question,
        value=nubby and quorum
    )


def out_of_sync_people_on_question_41(question: objects.Question) -> List[meta.Assertion]:
    """
    Identifies people who are out-of-sync on a question.

    Parameters
    ----------
    question

    Returns
    -------
    List[meta.Assertion]
        Values are True if person is out-of-sync on the question.
    """
    return disagreement.out_of_sync_people_on_question(question)


def significantly_out_of_sync_114(meeting: objects.Meeting,
                                  threshold_low=0.8,
                                  threshold_high=1.2) -> List[objects.Judgement]:
    """
    A person is out of sync on significantly higher number of questions than others in a meeting.
    # TODO: Figure out how to factor this better by Disentangling logic and data plumbing.
    # TODO: Where are parameters called and its default values set?

    Parameters
    ----------
    meeting
    threshold_low
    threshold_high

    Returns
    -------
    List[objects.Judgement]
        Value = True if person is Significantly OOS.
    """
    oos = {
        q.id: out_of_sync_people_on_question_41(q.id) for q in meeting.questions
    }

    oos_count = {
        person: 0 for person in meeting.partcipants
    }

    for q, is_oos in oos.items():
        for person in is_oos:
            if person.value:
                oos_count[person] += 1



    def to_zscore(x: Dict[objects.Person, int]) -> Dict[objects.Person, float]:
        """Placeholder.
        TODO: Find better home. analytics.foundation?
        TODO: Think through function signature.
        """
        pass

    oos_z_score = to_zscore(oos_count)
    results = []
    for person, v in oos_z_score:
        if notable_dict[person.id]:
            result_person = v > threshold_low
        else:
            result_person = v > threshold_high

        results += [
            objects.Judgement(source=objects.System, target=person, value=result_person)
        ]
    return results


    """
    A person is uniquely out of sync on a question, if their response is unique (
    analytics.disagreement.is_unique) and out-of-sync with the believable consensus (
    analytics.disagreement.out_of_sync_people_on_question).

    Parameters
    ----------
    question

    Returns
    -------
    List[meta.Assertion]
        Assertion for each person who answers the question. Value is whether they are uniquely
        out of sync.
    """
    unique_responses = disagreement.is_unique(question)
    oos = disagreement.out_of_sync_people_on_question(question)
    results = list()
    for person_unique in unique_responses:
        for person_oos in oos:
            if person_unique.target == person_oos.target:
                uniquely_oos = person_oos.value and person_unique.value
        results.append(meta.Assertion(source=objects.System, target=person_unique,
                                      value=uniquely_oos))
    return results
