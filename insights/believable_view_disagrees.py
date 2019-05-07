
"""
Believable View Disagrees With.
"""

import itertools
from prios_api.domain_objects import meta, objects
from prios_api.concepts import sentiment, disagreement


def believable_and_overall_meeting_section_sentiment_disagree_119(question: objects.Question) -> meta.Assertion:
    """
    Believable and Overall Meeting Section Sentiment Disagree

    TODO: This function assumes non-zero believabilities for every person

    Parameters
    ----------
    objects.Question
        The "Rate This Section" question object

    Returns
    -------
    meta.Assertion
        An assertion describing whether substantive disagreement exists between
        the believable and overall meeting section sentiment

    Examples
    --------
    >>> rate_the_section = objects.Question(title='Rate This Section', question_type=objects.QuestionType.RATING)
    >>> adam = objects.Person(name='Adam', believability=0.45)
    >>> bob = objects.Person(name='Bob', believability=0.05)
    >>> charlie = objects.Person(name='Charlie', believability=0.05)
    >>> rate_the_section.responses.append(objects.Response(source=adam, target=rate_the_section, value=10))
    >>> rate_the_section.responses.append(objects.Response(source=bob, target=rate_the_section, value=1))
    >>> rate_the_section.responses.append(objects.Response(source=charlie, target=rate_the_section, value=5))
    >>> result = believable_and_overall_meeting_section_sentiment_disagree_119(rate_the_section)
    >>> result.value
    1
    """
    assert question.question_type == objects.QuestionType.RATING, 'Question must be of type QuestionType.RATING!'

    responses = [(response.value, response.source.believability) for response in question.responses]
    values, weights = list(zip(*responses))

    believable_sentiment = sentiment.sentiment(values, weights=weights)
    overall_sentiment = sentiment.sentiment(values)

    result = disagreement.substantive_disagreement(believable_sentiment, overall_sentiment)
    return meta.Assertion(target=question, value=result)

#
# def believable_view_disagrees_with_overall_view_on_action_162(meeting: objects.Meeting):
#     """
#     TBD
#     """
#     # TODO: how do we roll-up an arbitrarily deep attribute taxonomy into actions?
#     # TODO: is the attribute taxonomy a function input?
#     # TODO: should a Meeting have actions (pre-populated) separately on the object? (YES)... why?
#     # TODO:    1) researchers will likely want to modify the taxonomy on the fly
#     # TODO:    2) hierarchical queries should be run on the server, not grpc
#     def sort_by_measure(x):
#         return x.measure.name
#
#     results = []
#     dots_by_attribute = sorted(meeting.dots.data, key=sort_by_measure)
#     for attribute, dot_set in itertools.groupby(dots_by_attribute, key=sort_by_measure):
#         materialized_dot_set = meta.EntityCollection(list(dot_set))  # TODO: materialization and instantiation is shitty here
#         result = believable_view_disagrees_with_overall_view_on_action(materialized_dot_set, attribute)
#         results.append(result)
#     return results
#
#
# def believable_view_disagrees_with_overall_view_on_action(dots: objects.DotCollection, attribute):
#     """
#     TBD
#     """
#     # TODO: This function assumes non-zero believabilities for every person
#     weights = [dot.source.believability for dot in dots]  # TODO: the data attribute is used confusingly; need dataclasses
#
#     if not weights:  # TODO: add better check that dots exist
#         return None
#
#     believable_view = sentiment.sentiment(dots, weights=weights)
#     overall_view = sentiment.sentiment(dots)
#
#     sentiment_comparison = (believable_view, overall_view)
#
#     result = disagreement.substantive_disagreement(sentiment_comparison)
#     return meta.Assertion(source=objects.System, target=attribute, value=result)
