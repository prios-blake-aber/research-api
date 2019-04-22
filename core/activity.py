
from src import objects


def action_relevance_158(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Defines a “Relevance” score for the Meeting Tracker Actions that were found to have occurred in a Meeting Section (see: [Actions in Meeting](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=156)) as a function of the number of of relevant Dots given.
    * Returns a Dictionary mapping [Actions in a Meeting](https://blakea-analytics-registry.dev.principled.io/detail?analytic=156) (Subject-Action pairs) to Relevance scores.
    * Returns Null if no Actions occurred in the Meeting.
    * This is produced by the following operation(s):
        * Selects Dots from the Meeting Section associated with each Action that occurred (relevant to the Subject-Action pair).
        * Calculates a “Relevance” score for each Action in a Meeting by counting the Dots given to the Subject on Attributes associated with the Action. Required Attributes count for twice as much
    """
    pass


def attention_participant_received_155(x: objects.Meeting):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Activity
    PROCESSING: Context-Only

    * Calculates the total number of Dots one Person received in a Poll Section
    * Returns a Statistic representing the Attention received by a Person
    """
    pass
