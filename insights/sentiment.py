
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


def author_opinions_on_actions_115(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Grouping
    PROCESSING: Context-Only

    * Groups the Dots of each Author in a Meeting by the Actions (a Meeting Tracker Action and the Subject who performed it) which which they are associated.
    * Returns a list of Author Opinions on Actions, which consist of the following:
       * The Author of the Opinions
       * The Subject of the Opinions
       * The Meeting Tracker Action in Question
       * A list of the Dots from the Author to the Subject on Attributes associated with the Action
       * A list of all Dots from any Meeting Participant to the Subject on Attributes associated with the Action
    * Returns an empty list if no Actions were identified in the Meeting.
    * This is produced by the following operation(s):
        * Maps Actions in a Meeting (Subject, Action pairs) to a list of the associated Meeting Dots.
        * For each Action, Maps the contributing Authors to their Dots on that Action.
        * Maps each Author of a Dot contributing to any of the Actions identified in the Meeting to the collection of information listed above.
    """
    pass


def author_view_on_action_152(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Grouping
    PROCESSING: Context-Only

    * Defines an Author’s view on how a Meeting Tracker Action was performed by a Subject as the average of the Dots that Author gave to the Subject on Attributes associated with the  Action.
    * Returns a Scale Value representing an Author’s view on how a Subject performed a Meeting Tracker Action.
    * Returns Null if called with an empty list - i.e. if the Person hasn’t authored any Dots to the Subject on Attribute associated with the Action.
    """
    pass


def believable_choice_130(x: objects.Question):
    """
    OUTPUT: Response
    INPUT: Believability
    CONTEXT: Question
    INSIGHT: Consensus
    PROCESSING: Context-Only

    * Defines "Believable Choice" as the [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16)-weighted majority opinion on a Question Response.
    * Returns the value representing the Believable Choice.
    * Returns Null if:
        * every Person responding to a Question has zero believability OR
        * for Categorical Responses, there is no choice receiving more than 70% of the believability-weighted vote.
    * This is produced by the following operation(s):
        * Calculates Total Believability: Calculates the sum of the Believability of all People who respond to a Question.
        * Determines the Believable Choice based on type of Response.
            * For Categorical or Yes/No Responses:
                * Calculates Response Believability for each Response: Calculates the sum of the Believability of People who give the same Response.
                * Calculates the ratio of Response Believability to Total Believability for each Response.
                * Determines whether the ratio above for any Response is greater than 0.70.
                * Selects the Response for which the above condition is True, if one exists. Returns Null otherwise.
            * For 1-to-10 or 1-to-5 scale Responses:
                * Calculates [believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16)-weighted average of responses.
    """
    pass


def believable_view_on_action_159(x: objects.AssertionSet):
    """
    OUTPUT: Person
    INPUT: Believability
    CONTEXT: AssertionSet
    INSIGHT: Believability
    PROCESSING: Context-Only

    * Defines the Believable View of an Action in a Meeting as the [Believability-Weighted Dots Mean](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=186) of all Dots associated with that Action - that is, all Dots received by a Subject on the Attributes associated with the Meeting Tracker Action.
    * Returns a Scale Value representing the Believable View of an Action.
    * Returns Null if called with an empty list - i.e. if no Meeting Participants have authored Dots to the Subject on Attributes associated with the Action.
    * This is produced by the following operation(s):
        * Calculates the Believable View of the Dots given to a Subject on Attributes associated with a Meeting Tracker Action using the [Believability-Weighted Dots Mean](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=186) method and passing in the Believability scores of the Dot Authors.
    """
    pass


def meeting_section_importance_34(x: objects.Meeting):
    """
    OUTPUT: Meeting
    INPUT: nan
    CONTEXT: Meeting
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Classifies Meeting Sections as Critical, Very Important, Important, Typical, or Unremarkable based on the number of Important People in the Meeting Section and the number of generated Dots and Questions.
    * Returns a Statistic between 0-1 that represents the classification of a Meeting Section's Importance.
    * This is produced by the following operation(s):
        * Calculates a Person Importance Value for each Participant based on their General Believability, and if provided, job level and whether they belong to particular Management Groups (job level and membership to management groups are not currently provided in the pilot). Defaults to zero.
        * Calculates the Important People Scaling Factor: calculates how many People had nonzero Person Importance (capped at 4).
        * Calculates the Activity Scaling Factor: calculates a statistic representing how much activity occurred in the Meeting Section based on Dots and Questions and achieves its maximum value at 100 Dots or 10 Questions.
        * Calculates the Dot Scaling Factor, which is a function of how many Dots were given in a Meeting Section and achieves its maximum value at 20 Dots.
        * Calculates the Total Importance: calculates the sum of all Meeting Section Participants' Person Importance.
        * Calculates the overall Meeting Section Importance Value: calculates the product of the Total Importance and the three Scaling Factors above.
        * Determines which classification the Meeting Section Importance Value receives and returns the associated text label (Critical, Very Important, Important, Typical, or Unremarkable).
    * To produce a result at the Meeting level (as opposed to Meeting Section Level), there is code living in the application which labels a Meeting based on the results from this analytic for the first Meeting Section only.
    """
    pass


def overall_meeting_section_quality_124(x: objects.Question):
    """
    OUTPUT: Meeting
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Defines "Meeting Section Quality" as the average of Rankings reflected in Question Responses to "Rate the Section".
    * Returns a Scale Value representing the Meeting Section Quality.
    * Returns Null if there are no "Rate the Section" Questions or Responses.
    * This is produced by the following operation(s):
        * Calculates the average of all Question Responses to "Rate the Section".
    """
    pass


def overall_meeting_section_sentiment_117(x: objects.Meeting):
    """
    OUTPUT: Meeting
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Defines "Overall Meeting Section Sentiment" as the [Dots Summary](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=186) of all Dots in a Meeting.
    * Returns a Scale Value representing Overall Meeting Section Sentiment.
    * Returns Null if there are no Dots in the Poll.
    """
    pass


def believable_meeting_section_quality_123(x: objects.Question):
    """
    OUTPUT: Response
    INPUT: Believability
    CONTEXT: Question
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Defines "Believable Meeting Section Quality" as the [Believability-weighted](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) average of Rankings reflected in Question Responses to "Rate the Section".
    * Returns a Scale Value representing the [Believable](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) Meeting Section Quality.
    * Returns Null if there are no "Rate the Section" Questions or Responses.
    * This is produced by the following operation(s):
        * Maps [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) to 0.01 for people who don't have that Score.
        * Calculates the [Believability-weighted](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) average of all Question Responses to  "Rate the Section".
    """
    pass


def believable_meeting_section_sentiment_116(x: objects.Meeting):
    """
    OUTPUT: Meeting
    INPUT: Believability
    CONTEXT: Meeting
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Defines "Believable Meeting Section Sentiment" as the [Believable Dots Summary](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=186) of all Dots in a Meeting.
    * Returns a Scale Value representing the Believable Meeting Section Sentiment.
    * Returns Null if there are no Dots in the Meeting.
    * This is produced by the following operation(s):
        * Calculates the Believability-Weighted Author-Capped Dot Average: Combines Dot values with a weighted average, using the product of the Author's [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=14) and [Capped Author Weights](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=171) as weights.
    """
    pass


def dotted_notably_poorly_in_meeting_127(x: objects.Meeting):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Identifies whether a given Subject across all Attributes receives a Negative [believability-weighted](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) Dot average and no Positive Dots in a Meeting Section.
    * Returns a Boolean representing whether a Person was Dotted Notably Poorly in a Meeting across all Attributes in a Meeting Section.
    * This is produced by the following operation(s):
        * Calculates the [believability-weighted](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) mean of all Dots across all Attributes in a Meeting section.
        * Determines whether the [believability-weighted](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) Attribute Dot mean is Negative.
        * Determines whether there are no Positive Dots.
        * Determines whether both of the previous conditions are True.
    """
    pass


def dotted_notably_well_in_meeting_126(x: objects.Meeting):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Identifies whether a given Subject across all Attributes receives a Very Positive (>8) [Believability-weighted](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) Dot average and no Negative Dots in a Meeting Section.

    * Returns a Boolean representing whether a Person was Dotted Notably Well in a Meeting across All Attributes in a Meeting Section.

    * This is produced by the following operation(s):

        * Calculates the [Believability-weighted](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) mean of all Dots across all Attributes in a Meeting Section.

        * Determines whether the [Believability-weighted](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) Dot mean is Very Positive (>8).

        * Determines whether there are no Negative Dots.

        * Determines whether both of the previous conditions are True.
    """
    pass


def frequent_negatively_dotted_attributes_31(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Selects up to 3 weakest Attributes from those on which a Person has 10 or more Dots averaging 5.5 or less.
    * Returns a List of up to 3 Attributes that represent a Person's Frequent Negatively Dotted Actions.
    * Returns an empty list if a Person has not received more than 10 Dots on any single Attribute or if they don't have any Attributes with an average Dot value less than 5.5.
    * This is produced by the following operation(s):
        * Determines if a Person has received at least 10 Dots on an Attribute.
        * Calculates the average of all Dots received on the Attributes from the previous step.
        * Determines if any Attributes' averages from the previous step are less than 5.5.
        * Selects top 3 Attributes from an ascending sorted list of Attributes based on the averages from the previous step (if ties exist, they are broken arbitrarily).
    """
    pass


def frequent_positively_dotted_attributes_30(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Selects up to 3 highest rated Attributes from those on which a Person has 10 or more Dots averaging 6.5 or better.
    * Returns a List of up to 3 Attributes that represent a Person's Frequent Positively Dotted Actions.
    * Returns an empty list if a Person has not received more than 10 Dots on any single Attribute or if they don't have any Attributes with an average Dot value greater than 6.5.
    * This is produced by the following operation(s):
        * Determines if a Person has received at least 10 Dots on an Attribute.
        * Calculates the average of all Dots received on the Attributes from the previous step.
        * Determines if any Attributes' averages from the previous step exceed 6.5.
        * Selects top 3 Attributes from a descending sorted list of Attributes based on the averages from the previous step (if ties exist, they are broken arbitrarily).
    """
    pass


def negatively_dotted_attributes_in_meeting_121(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Identifies Attributes on which a Subject received Negative Dots in a Meeting.
    * Returns a List of Attributes representing the Negatively Dotted Attributes in Meeting for a Participant.
    * Returns an empty list if there are no Negative Dots.
    * This is produced by the following operation(s):
        * Determines whether each Dot was Negative.
        * Selects the list of Attributes that had at least one Negative Dot.
    """
    pass


def positively_dotted_attributes_in_meeting_120(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Identifies Attributes on which a Subject received Positive Dots in a Meeting.
    * Returns a List of Attributes representing Positively Dotted Attributes in Meeting.
    * Returns an empty list if there are no Positive Dots.
    * This is produced by the following operation(s):
        * Determines whether each Dot was Positive.
        * Selects Attributes that had at least one Positive Dot.
    """
    pass
