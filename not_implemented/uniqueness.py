
from src import objects


def unexpected_action_163(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Comparing [Believable vs. All-Stream]

    * Identifies whether the [Believable View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=159) on an Action in a Meeting [Substantively Disagrees](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) with the [Expected View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=165) derived from the Subject’s All-Stream scores.
    * Returns a Boolean representing the above.
    * This is produced by the following operation(s):
      * Compares the [Expected View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=165) to the [Believable View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=159) using the [Substantive Disagreement](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) library method.
    """
    pass


def author_disagrees_with_believable_view_on_action_153(x: objects.AssertionSet):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Disagreement
    PROCESSING: Comparing [Person vs. Believable]

    * Identifies when an Author’s View of an Action in a Meeting [Substantively Disagrees](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) with the Believable View.
    * Returns a Boolean indicating the above.
    * This is produced by the following operation(s):
        * Compares the Author’s View to the Believable View using the [Substantive Disagreement](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) library method
    """
    pass


def author_disagrees_with_overall_view_on_action_154(x: objects.AssertionSet):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Disagreement
    PROCESSING: Comparing [Person vs. Overall]

    * Identifies when an Author’s View of an Action in a Meeting [Substantively Disagrees](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) with the [Overall View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=160).
    * Returns a Boolean indicating the above.
    * This is produced by the following operation(s):
        * Compares the Author’s View to the [Overall View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=160) using the [Substantive Disagreement](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) library function.
    """
    pass


def disagreeing_dotters_higher_than_average_111(x: objects.AssertionSet):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Disagreement
    PROCESSING: Comparing [Person vs. Overall]

    * Identifies Authors whose average opinion of a Subject across all Attributes is one of the five highest of all Authors, and is at least 2.0 more than the average Dot the Subject received.
    * Returns a list of People that represent Disagreeing Dotters (Higher Than Average).
    * Returns an empty list if the Subject hasn’t received any Dot Ratings or if no Dot Authors meet the criteria below.
    * This is produced by the following operation(s):
        * Calculates the average of all Dot Ratings that the Subject receives and the average of each Author’s Dot Ratings of the Subject.
        * Determines whether each Author’s average Dot Rating exceeds the average of all Dot Ratings that the Subject receives by at least 2.0.
        * Determines whether each Author’s Dot Rating average is among the five highest of all Authors’ average Dot Ratings of the Subject.
        * Selects the Authors for which the previous two conditions are both True.

    """
    pass


def disagreeing_dotters_lower_than_average_24(x: objects.AssertionSet):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Disagreement
    PROCESSING: Comparing [Person vs. Overall]

    * Identifies Authors whose average opinion of a Subject across all Attributes is one of the five lowest of all Authors, and is at least 2.0 less than the average Dot the Subject received.
    * Returns a list of People that represent Disagreeing Dotters (Lower Than Average).
    * Returns an empty list if the Subject hasn’t received any Dot Ratings or if no Dot Authors meet the criteria below.
    * This is produced by the following operation(s):
        * Calculates the average of all Dot Ratings that the Subject receives and the average of each Author’s Dot Ratings of the Subject.
        * Determines whether each Author’s average Dot Rating is 2.0 or lower than the average of all Dot Ratings that the Subject receives.
        * Determines whether each Author’s Dot Rating average is among the five lowest of all Authors’ average Dot Ratings of the Subject.
        * Selects the Authors for which the previous two conditions are both True.

    """
    pass


def significantly_out_of_sync_people_on_question_114(x: objects.Meeting):
    """
    OUTPUT: Person
    INPUT: Responses
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Comparing [Person vs. Believable]

    * Identifies People who disagree with the believable choice on substantially more questions than others during a Meeting.
    * Returns List of People representing those who are Significantly Out of Sync People on Question.
    * Returns an empty List if no Person in the Meeting Section satisfies conditions below.
    * This is produced by the following operation(s):
        * Calculates the count of questions on which each Person was [Out of Sync with the Believable Consensus](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=41).
        * Calculates Z-scores of the counts over all People in a Meeting Section.
        * Determines whether each Person was Notable: Combines the following conditions:
            * Determines whether a Person is a [Primary Meeting Participant](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=138).
            * Determines whether a Person's [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) is greater than zero.
        * Determines whether a Person is Significantly Out of Sync: Combines the following conditions:
            * A Person is Notable and their Z-score is greater than the Notable threshold (0.67).
            * A Person is Not Notable and their Z-score is greater than the General threshold (1.28).
        * Selects People who are Significantly Out of Sync.
    """
    pass
