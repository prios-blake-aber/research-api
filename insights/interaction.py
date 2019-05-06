
"""
TBD
"""

import itertools
from src import objects, meta
from prios_api import sentiment, disagreement


def believable_and_overall_meeting_section_sentiment_disagree_119(question: objects.Question):
    """
    TBD
    """
    # TODO: This function assumes non-zero believabilities for every person
    weights = [response.source.believability for response in question.responses.data]

    believable_sentiment = sentiment.sentiment(question.responses, weights=weights)
    overall_sentiment = sentiment.sentiment(question.responses)

    sentiment_comparison = (believable_sentiment, overall_sentiment)

    result = disagreement.substantive_disagreement(sentiment_comparison)
    return meta.Assertion(source=objects.System, target=question, value=result)


def believable_view_disagrees_with_overall_view_on_action_162(meeting: objects.Meeting):
    """
    TBD
    """
    # TODO: how do we roll-up an arbitrarily deep attribute taxonomy into actions?
    # TODO: is the attribute taxonomy a function input?
    # TODO: should a Meeting have actions (pre-populated) separately on the object? (YES)... why?
    # TODO:    1) researchers will likely want to modify the taxonomy on the fly
    # TODO:    2) hierarchical queries should be run on the server, not grpc
    def sort_by_measure(x):
        return x.measure.name

    results = []
    dots_by_attribute = sorted(meeting.dots.data, key=sort_by_measure)
    for attribute, dot_set in itertools.groupby(dots_by_attribute, key=sort_by_measure):
        materialized_dot_set = meta.EntityCollection(list(dot_set))  # TODO: materialization and instantiation is shitty here
        result = believable_view_disagrees_with_overall_view_on_action(materialized_dot_set, attribute)
        results.append(result)
    return results


def believable_view_disagrees_with_overall_view_on_action(dots: objects.DotCollection, attribute):
    """
    TBD
    """
    # TODO: This function assumes non-zero believabilities for every person
    weights = [dot.source.believability for dot in dots.data]  # TODO: the data attribute is used confusingly; need dataclasses

    if not weights:  # TODO: add better check that dots exist
        return None

    believable_view = sentiment.sentiment(dots, weights=weights)
    overall_view = sentiment.sentiment(dots)

    sentiment_comparison = (believable_view, overall_view)

    result = disagreement.substantive_disagreement(sentiment_comparison)
    return meta.Assertion(source=objects.System, target=attribute, value=result)
