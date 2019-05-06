
"""
TBD
"""

from typing import List, Dict
from prios_api.domain_objects import meta, objects
from prios_api import utils, disagreement, activity


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
def action_is_polarizing_161(meeting: objects.Meeting,
                             by_action: Dict[str, str] = None) -> List[meta.Assertion]:
    """
    Identifies Meeting Tracker Actions in a Meeting that are polarizing.

    TODO: Reconcile with:
    insights.interaction.believable_view_disagrees_with_overall_view_on_action_162

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
        Whether or not Dots are polarizing (by action). Action is indexed in the label attribute.
    """
    return disagreement.dots_in_meeting_are_polarizing(meeting, by_action=by_action)


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


def believable_consensus_exists_131(question: objects.Question) -> meta.Assertion:
    """
    Whether consensus exists on a question.

    Parameters
    ----------
    question

    Returns
    -------
    bool
        Whether there is a consensus answer.
    """
    return disagreement.believable_consensus_exists(question)


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
