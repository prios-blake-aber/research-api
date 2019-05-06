
"""
TBD
"""

from typing import List
from src import objects, meta
from analytics import disagreement


def uniquely_out_of_sync_on_question_136(question: objects.Question) -> List[meta.Assertion]:
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
