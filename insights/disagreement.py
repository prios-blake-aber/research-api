
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
def meeting_section_sentiment_is_polarizing_118(meeting: objects.Meeting) -> objects.Judgement:
    """
    Determines if Meeting Section Sentiment is polarizing, based on Dots.

    Parameters
    ----------
    meeting

    Returns
    -------
    objects.Judgement
    """
    dots = [dot for dot in meeting.dots]
    return disagreement.is_polarizing(dots)


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


@utils.scope_required_data_within_object(collections_to_keep=['participants', 'questions'])
def quorum_exists_in_meeting(meeting: objects.Meeting,
                             quorum_threshold: float = _QUORUM_THRESH_DEFAULT,
                             *args, **kwargs) -> List[meta.Assertion]:
    """
    Determines whether a sufficient percentage of Participants answered each question
    asked during a Meeting.

    Parameters
    ----------
    meeting
    quorum_threshold : The threshold above which quorum exists. Defaults to :data:`_QUORUM_THRESH_DEFAULT`
    *args: Variable length argument list.
    **kwargs: Arbitrary keyword arguments.

    Returns
    -------
    List[meta.Assertion]
        Value is True if Quorum exists on respective question. V
    """
    number_participants = activity.participants(meeting)
    return [
        activity.quorum_exists_on_question_145(question, number_participants=number_participants,
                                               quorum_threshold=quorum_threshold)
        for question in meeting.questions.data
    ]


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
    polarizing = disagreement.polarizing_topics(meeting.dots)

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

    TODO: Move logic to analytics.

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
    notable = activity.notable_participants(meeting)
    # TODO: Util function to convert List of Assertions to Dictionary (doable with Dataclasses)
    notable_dict = {
        p.id: p.value for p in notable
    }

    oos = {
        q.id: out_of_sync_people_on_question_41(q.id) for q in meeting.questions
    }

    oos_count = {
        person: 0 for person in meeting.partcipants
    }

    for k, v in oos:
        for person in v:
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
