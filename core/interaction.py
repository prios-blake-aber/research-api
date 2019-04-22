
from src import objects


def negative_dot_on_a_better_subject_popup_46(x: objects.Meeting):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Comparing [Dots vs. All-Stream]

    * Notifies a Person when they give Negative Dots in a Meeting to a Subject with an All-Stream score substantially higher than their own on the Attribute in question (difference in percentiles > 40%).
    * Returns a Boolean representing whether a Person gave a Negative Dot to a Subject who is Better than them.
    * Returns Null if a Person does not have an All Stream score on that Attribute.
    * This is produced by the following operation(s):
        * Calculates the difference in the Subject and Author's All Stream percentiles on the Attribute.
        * Determines whether the difference in the Subject and Author's All Stream percentiles on the Attribute is greater than 40%.
        * Determines whether a Subject gave a Negative Dot (<5).
        * Determines whether there is Sufficient Confidence (at least 1.2) associated with the Author and Subject's All Stream scores using [Stream Population Summary Confidence](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=140) for that Attribute.
        * Combines the previous 3 conditions.
    """
    pass


def meeting_section_quality_is_polarizing_125(x: objects.Question):
    """
    OUTPUT: Meeting
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Identifies whether Rankings of a Meeting Section's usefulness are [Polarizing](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=141) based on "Rate the Section" Responses.
    * Returns a Boolean representing whether Question Responses to "Rate the Section" are [Polarizing](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=141).
    * This is produced by the following operation(s):
        * Tests whether the "Rate the Section" Question Responses in a Meeting Section are Polarizing using the [Polarizing](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=141) library function.
    """
    pass


def believable_and_overall_meeting_section_quality_disagree_143(x: objects.Question):
    """
    OUTPUT: Response
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Comparing [Believable vs. Overall]

    * Identifies whether the [Believable Meeting Section Quality](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=123) [Substantially Disagrees](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) with the [Meeting Section Quality](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=124), based Question Responses to "Rate the Section".
    * Returns a Boolean representing whether the [Believable Meeting Section Quality](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=123) [Substantially Disagrees](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) with the [Meeting Section Quality](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=124)
    * This is produced by the following operation(s):
        * Calculates the [Believable Meeting Section Quality](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=123) from "Rate the Section" Question Responses and Authors' Believability scores.
        * Calculates the [Meeting Section Quality](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=124) from "Rate the Section" Question Responses.
        * Tests for Substantial Disagreement between the [Believable Meeting Section Quality](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=123) and the [Meeting Section Quality](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=124) using the [Substantial Disagreement](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) library function.
    """
    pass


def believable_and_overall_meeting_section_sentiment_disagree_119(x: objects.Meeting):
    """
    OUTPUT: Meeting
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Sentiment, Disagreement
    PROCESSING: Comparing [Believable vs. Overall]

    * Identifies Meetings in which the [Believable Meeting Section Sentiment](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=116) [Substantively Disagrees](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) with the [Overall Meeting Section Sentiment](https://blakea-analytics-registry.dev.principled.io/detail?writeup=117).
    * Returns a Boolean representing whether the Believable and Overall Meeting Section Sentiment Disagree.
    """
    pass


def believable_sentiment_disagrees_with_overall_sentiment_142(x: objects.Meeting):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Comparing [Believable vs. Overall]

    * Identifies Notable Poll Section Participants on which there was [Substantive Disagreement](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) between the Believable View and the Overall View.
    * Returns a Boolean representing the above.
    * This is produced by the following operation(s):
       * Assumes that all Poll Section Dots on a Participant who was found to have performed Notably [Well](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=126) / [Poorly](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=127) have been passed in.
       * Calculates the Believable View using the [Weighted Dots Mean method](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=186) and passing in the Believability scores of the Dot Authors.
       * Calculates the Overall View using the [Weighted Dots Mean method](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=186)
       * Determines whether there is Substantive Disagreement between the two Views using the [Substantive Disagreement library method](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129)

    """
    pass


def believable_view_disagrees_with_overall_view_on_action_162(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Comparing [Believable vs. Overall]

    * Identifies Actions in Meetings about which there is [Substantive Disagreement](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) between the [Overall View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=117) and the [Believable View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=116).
    * Returns a Boolean representing the above.
    * This is produced by the following operation(s):
      * Compares the [Overall View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=117) to the [Believable View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=116) using the [Substantive Disagreement](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=129) library method.
    """
    pass
