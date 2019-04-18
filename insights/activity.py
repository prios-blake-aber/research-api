
from src import objects


def actions_in_meeting_156(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Activity
    PROCESSING: Context-Only

    * Selects Meeting Tracker Actions performed by Subjects in Meeting Sections by inspecting the Dots given.
    * Returns a List representing of all Actions which Have Occurred, where each list item is a Subject and Action pair.
    * Returns Null if no Actions have occurred.
    * This is produced by the following operation(s):
        * A Subject is deemed to have performed a Meeting Tracker Action during a Meeting Section if he or she received Dots on any of the Attributes defined as Required Attributes of the Action.  Determines which, if any, Meeting Tracker Actions occurred in a Meeting Section by checking the Dots given to each Subject against the list of Required Attributes for each Meeting Tracker Action.
        * Selects unique Subject and Action pairs matching the previous condition.
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


def primary_actions_157(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Activity
    PROCESSING: Context-Only

    * Selects the Actions that are considered Primary in a Meeting, based on their [Relevance scores](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=158).
    * Returns a list of Actions from a Meeting that are considered Primary.
    * Returns an empty list if there were no Actions in the Meeting.
    * This is produced by the following operation(s):
        * Assumes the list of Participants is already sorted by total number of Dots received (on Attributes associated with each Participant’s Actions).
        * Maps each Participant with Actions in the Meeting to a list of their Actions.
        * Sorts each Participant’s list of Actions by the [Relevance score](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=158).
        * Selects up to a configurable maximum number of Primary Actions, choosing the next most relevant action from each Participant in a round robin fashion.
    """
    pass


def primary_participants_in_meeting_138(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Activity
    PROCESSING: Comparing [Person vs. Overall]

    * Identifies whether a Person received more than 20% of Dots (or more than 10% of Dots if they receive at least 10 Dots) during a Meeting
    * Returns a boolean representing whether a Person is a Primary Participant in a Meeting.
    * This is produced by the following operation(s):
        * Determines whether a Person is a Primary Participant in a Meeting if either of the following conditions are true:
         * Determines whether a Person received more than 20% of Dots in a Meeting
         * Determines whether a Person received more than 10% of Dots and more than 10 Dots in a Meeting
    """
    pass
