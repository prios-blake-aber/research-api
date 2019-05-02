
from src import objects
from analytics import utils, activity, disagreement

"""
Polarizing - distribution at the poles
Divisiveness - standard deviation
Nubbiness - divisiveness with "enough" observations
Consensus
"""


def action_is_polarizing_161(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Identifies Meeting Tracker Actions in a Meeting that are [polarizing](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=141) based on Dots associated with the Action.
    * Returns a Boolean representing whether an Action in a Meeting Is Polarizing.
    """
    pass


@utils.scope_required_data_within_object(collections_to_keep=['dots'])
def meeting_section_sentiment_is_polarizing_118(meeting: objects.Meeting):
    """
    OUTPUT: Meeting
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Sentiment, Disagreement
    PROCESSING: Context-Only

    * Identifies Meetings in which the sentiment based on all Dots is [Polarizing](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=141).
    * Returns a Boolean representing whether the Meeting Sentiment is Polarizing.
    """
    dots = [dot for dot in meeting.dots]
    return disagreement.is_polarizing(dots)


def is_polarizing_141(x: objects.AssertionSet):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Identifies a Polarizing event when Scale Values on a Person are spread out and there exist comparable numbers of positive (8 and above) and negative (4 and below) Scale Values
    * Returns a boolean
    * This is produced by the following operation(s):
        * Calculates the standard deviation of Scale Values
        * Calculates the Bucketed Standard Deviation of Scale Values:
            * Maps the Scale Values to their Summarized Opinion
            * Calculates the standard deviation
        * Calculates the Relative Incidence Ratio of positive/negative Scale Values
            * Calculates the numerator as the minimum count of positive/negative Scale Values
            * Calculates the Denominator as the maximum count of positive/negative Scale Values
        * Combines the following conditions to determine whether the Scale Values are polarizing:
            * Calculates the standard deviation of Scale Values is greater than 0.5
            * Calculates the Bucketed Standard Deviation of Scale Values is greater than 1.0
            * Calculates the Relative Incidence Ratio of positive/negative Scale Values is greater than 0.25
    """
    pass


def disagrees_with_167(x: objects.Question):
    """
    OUTPUT: Response
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Comparing [Collections of People]

    * Defines "Disagreement" between two opinions on a Question. Two opinions disagree when they are classified into different [groups](https://blakea-analytics-registry.dev.principled.io/detail?analytic=168) and, if they are Question Responses with Likert or Scale Values, also have a difference greater than a configurable threshold (with a default value of 1.7).
    * Returns a Boolean representing whether two opinions Disagrees With one another.
    * This is produced by the following operation(s):
        * Determines whether two opinions disagree as:
            * For Categorical or Yes/No opinions: the two opinions are different.
            * For Likert or Scale Value opinions:
                * Determines whether the two opinions are Far Away: Compares whether the difference is greater than a configurable threshold value (default value of 1.7).
                * Maps each opinion to a Summarized Opinions (Negative, Neutral, or Positive).
                * Determines whether the Summarized Opinions Disagree: Determines whether their values are different.
                * Determines whether the two opinions are Far Away and their Summarized Opinions Disagree.
    """
    pass


def divisiveness_179(x: objects.Question):
    """
    OUTPUT: Response
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Defines Divisiveness as the standard deviation of Summarized Opinions reflected in Meeting Question responses.
    * Returns a Statistic representing Divisiveness.
    * Returns Null in the following cases:
        * Fewer than two People respond to a Question.
        * The Question has Categorical Responses.
    * This is produced by the following operation(s):
        * Maps opinions to [Summarized Opinions](https://blakea-analytics-registry.dev.principled.io/detail?analytic=168).
        * Calculates the standard deviation of the Summarized Opinions.
    """
    pass


def contradictory_action_164(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Disagreement
    PROCESSING: Comparing [Believable vs. All-Stream]

    * Identifies whether the [Believable View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=159) on an Action in a Meeting contradicts the [Expected View](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=165) derived from the Subject’s All-Stream scores - that is, whether one view is Negative while the other is Positive.
    * Returns a Boolean representing the above.
    * This is produced by the following operation(s):
        * Buckets the Believable and Expected Views on the Action into Summarized Opinions - Negative, Neutral, and Positive.
        * Determines whether one View is Negative while the other is Positive.
    """
    pass


def partition_teams_128(x: objects.Meeting):
    """
    OUTPUT: Person
    INPUT: Responses
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Comparing [Collections of People]

    * Identifies Managers (Person managing a Team) whose Team predominantly (greater than 60%) agreed with them
    * Returns a map of Responses to sets of Managers (Person managing a Team) whose Team sided with them.
    * This is produced by the following operation(s):
        * Selects sets of Managers (Person managing a Team) who meet the following conditions:
            * Determines when more than 3 people on the Team responded
            * Determines when more than 60% of the Team responded in the same way as the Manager (Person managing a Team)
        * Maps Responses to Managers whose Teams agreed with them on that Response
    """
    pass


def substantive_disagreement_129():
    """
    This is a building-block function.

    OUTPUT: Response
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Identifies a pair of Scale Values that Substantively Disagree.
    * Returns a Boolean representing whether Substantive Disagreement exists.
    * This is produced by the following operation(s):
        * Calculates the absolute difference between the two values.
        * Determines whether the values are Far Away: Compares whether the difference is greater than a threshold of 1.7.
        * Maps Responses into Summarized Opinions.
        * Determines whether the Summarized Opinions Disagree: determines whether their values are different.
        * Returns True if both of the above conditions are True.
    """
    pass


def consensus_exists_131(x: objects.Question):
    """
    OUTPUT: Response
    INPUT: Believability
    CONTEXT: Question
    INSIGHT: Consensus
    PROCESSING: Context-Only

    * Identifies whether the [believability-weighted](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) vote on a Question exceeds 90% for one Response.
    * Returns a Boolean representing Believable Consensus Exists.
    * This is produced by the following operation(s):
        * Calculates Total Believability: Calculates the sum of the [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) of all People who respond to a Question.
        * Calculates Response Believability for each possible Response: Calculates the sum of the [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) of People who give the same Response.
        * Determines whether there is Agreement Among Believable Respondents: determines whether the ratio of Response Believability to Total Believability exceeds $0.9$ for any Response.
        * Determines whether there are Enough Respondents: determines whether there are more than $3$ People who give Responses.
        * Determines whether there is Sufficient Believability: determines whether Total Believability exceeds $0.75$.
        * Determines whether the previous three conditions are True.
    """
    pass


def meeting_section_nubbiness_149(x: objects.Meeting):
    """
    OUTPUT: Meeting
    INPUT: Question
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Classifies Meeting Sections as Very Nubby, Nubby, Somewhat Nubby, Less Nubby and Not Nubby based on the number of [Nubby Questions](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=40) in the Meeting and how much disagreement there was in each Question.
    * Returns a Statistic between 0-1 that represents a classification of a Meeting Section's Nubbiness.
    * This is produced by the following operation(s):
        * Calculates the Nubby Question Scaling Value:
           * Calculates the product of 0.5 and the number of Nubby Questions.
           * Determines the minimum between 1 and the result of the previous step.
        * Calculates the Meeting Section [Divisiveness](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=179).
        * Calculates the product of the Nubby Question Scaling Value and Meeting Section Divisiveness.
        * Determines which classification to apply from a list of labels.
    * To produce a result at the Meeting level (as opposed to Meeting Section Level), there is code living in the application which labels a Meeting based on the results from this analytic for the first Meeting Section only.
    """
    pass


def nubby_attributes_in_meeting_39(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Identifies all Attribute-Subject pairs for which Dotters in a Meeting Section gave conflicting Dots.
    * Returns a Dictionary mapping Attributes to  Lists of People, that represents Subjects whose Dots on the respective Attribute was viewed as being Nubby.
    * Returns an empty mapping if no Subject was deemed to have a Nubby Attribute based on criteria below.
    * This is produced by the following operation(s):
        * Determines whether a Subject receives at least 5 Dots on an Attribute.
        * Determines whether a Subject received a substantial portion of their Dots about an Attribute :
             *  Calculates the Attribute Ratio: the number of Dots that a Subject receives on an Attribute divided by the number of Dots that a Subject receives on all Attributes.
             * Calculates the number of unique triples of an Author giving a Dot to a Subject on an Attribute.
             *  Calculates the Author Ratio: the number of unique Author-Subject-Attribute triples divided by the number of Authors who gave a Dot to the Subject.
             * Determines whether the Attribute Ratio is greater than 0.05.
             * Determines whether Authors Frequently Dot Subject on an Attribute if either of the following are True:
                  * The Author Ratio is greater than 0.2 or there are at least 10 unique Author-Subject-Attribute triples.
                  * The Attribute Ratio is greater than 0.33.
             * Determines whether the two conditions above are True.
        * Calculates each Author's average Dot Rating on the Subject about an Attribute.
        * Determines whether an Attribute of a Subject is viewed as being Polarizing from Dot Ratings that they receive:
            * Calculates each Author's Synthesized View of the Subject: Calculates the average of the Author's Dot Ratings on a Subject about an Attribute.
            * Maps each Author's Synthesized View of the Subject to Summarized Synthesized Views (Negative, Neutral, or Positive).
            * Determines whether the proportions of Positive and Negative views are roughly equal: both of the following conditions must hold:
                * The ratio of the number of Positive views to the number of Neutral views exceeds 0.25.
                * The ratio of the number of Negative views to the number of Positive views exceeds 0.25.
            * Determines whether the standard deviation of Authors' Synthesized Views exceeds 1.
            * Determines whether the standard deviation of Authors' Summarized Synthesized Views exceeds 0.5 (after mapping Negative Views to 1, Neutral Views to 2, and Positive Views to 3).
            * Determines whether the three conditions above are all True.
        * Determines whether the three conditions above (Subject's Attribute is Polarizing, Subject receives at least 5 Dots on an  Attribute, and Subject received a substantial portion of their Dots about an Attribute) are all True.
        * Selects Subject-Attribute pairs where the condition above is True.
    """
    pass


def nubby_people_in_meeting_38(x: objects.Meeting):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Selects all People who are viewed as being [polarizing](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=141)  based on Dots in a Meeting Section.
    * Returns a list of People who were identified as Nubby People in Meeting.
    * Returns an empty list if there are no Subjects whose Dot Ratings satisfy the criteria below.
    * This is produced by the following operation(s):
        * Calculates the number of Dots that a Subject receives.
        * Calculates the percent of Dots that a Subject receives as a fraction of all Dots given in a Meeting Section.
        * Determines whether a Subject is Frequently Dotted: receives more than either:
            * 10% of all Dot Ratings OR
            * 5% of all Dot Ratings along with 10 Dot Ratings.
        * Determines whether a Subject is viewed as being [Polarizing](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=141) from Dot Ratings that they receive:
            * Calculates each Author's Synthesized View of the Subject: Calculates the average of the Author's Dot Ratings on a Subject.
            * Maps each Author's Synthesized View of the Subject to Summarized Synthesized Views (Negative, Neutral, or Positive).
            * Determines whether the proportions of Positive and Negative view are roughly equal: both of the following conditions must hold:
                * The ratio of the number of Positive views to the number of Neutral views exceeds 0.25.
                * The ratio of the number of Negative views to the number of Positive views exceeds 0.25.
            * Determines whether the standard deviation of Authors' Synthesized Views exceeds 1.
            * Determines whether the standard deviation of Authors' Summarized Synthesized Views exceeds 0.5 (after mapping Negative Views to 1, Neutral Views to 2, and Positive Views to 3).
            * Determines whether the three conditions above are all True.
        * Determines whether a Subject is both Frequently Dotted and Polarizing.
        * Selects all Subjects that satisfy the condition above.
    """
    pass


def nubby_question_147(x: objects.Question):
    """
    OUTPUT: Question
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Defines a Nubby Question as one where there is a disagreement between People who Respond to it.
    * Returns a Boolean representing whether the Question is Nubby.
    * Returns False if fewer than 2 People responded to a Question.
    * This is produced by the following operation(s):
        * Calculates Question Divisiveness, which depends on the type of Question Response:
            * For Response types with Scale Values, Likert Values, or Yes/No Values: Calculates [Divisiveness](https://blakea-analytics-registry.dev.principled.io/detail?analytic=179) from Responses to a Question.
            * For Categorical response types:
                 * Determines the Most Common Choice: Choice with highest proportion of Responses.
                 * Maps responses of the Most Common Choice to 1 and all other Responses (including N/A's) to 2.
                 * Calculates the standard deviation of the mapped Responses.
        * Determines whether Question Divisiveness exceeds a configurable threshold which depends on the Response Type:
            * 0.5 for Categorical, Yes/No, Scale, and Likert Value Responses
            * 1.0 for Numerical Valued Responses
    """
    pass


def percent_chance_responder_is_wrong_popup_144(x: objects.Question):
    """
    OUTPUT: Person
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Comparing [Person vs. Believable]

    * Notifies People who [disagree](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=167) with the [Believable Choice](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=130) on a Question. It also informs them of the percentage of the [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16)-weighted vote going to the Believable Choice.
    * Returns a mapping of each Person to a Statistic, which represents their Percent Chance of Being Wrong.
    * Returns a mapping of each Person to zero if any of the following conditions are True:
        * There is no Believable Choice Response.
        * People who Respond do not have Sufficient Believability.
        * No Person disagrees with the Believable Choice.
    * This is produced by the following operation(s):
        * Calculates the Total Participant Believability as the sum of the [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) of every Person in a Meeting Section and the Total Response Believability as the sum of the Believability of every Person who responded to the Question.
        * Calculates the Response Believability Ratio as the ratio of the Total Response Believability to the Total Participant Believability.
        * Determines whether there is Sufficient Believability in Responses if the following are both true:
            * The Response Believability Ratio is greater than 0.8.
            * The Total Participant Believability is greater than 0.
        * Calculates the [Believable Choice](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=130).
        * Determines whether each Person [Disagrees With](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=167) the Believable Choice.
        * Determines whether a "Person is Wrong" by assessing if both conditions below are both True:
            * There exists Sufficient Believability.
            * The Person Disagrees with the Believable Choice.
        * Defines a Person's Believability Adjustment Factor as:
            * A small fixed positive quantity if a Person's Believability is greater than zero.
            * Zero if a Person's Believability equals zero.
        * Defines the Adjusted Believability for each Person as the sum of each Person's Believability and Believability Adjustment Factor.
        * Calculates the "Adjusted Believability in Agreement with the Believable Choice" as the sum of Adjusted Believability of People who agree with the Believable Choice.
        * Calculates the "Total Adjusted Believability" as the sum of Adjusted Believability of all People.
        * Calculates the Percent Chance of Being Wrong as the minimum of the following two quantities:
            * Ratio of "Adjusted Believability in Agreement with Believable Choice" to the "Total Adjusted Believability".
            * A transformation of Total Adjusted Believability to a value between 0.5 and 1.
        * Maps the following quantities to each Person depending on whether the "Person is Wrong":
            * "Percent Chance of Being Wrong" if "Person is Wrong" is True.
            * Zero if "Person is Wrong" is False.
    """
    pass


def not_perceiving_problems_popup_47(x: objects.Meeting):
    """
    OUTPUT: Person
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Activity, Disagreement
    PROCESSING: Comparing [Person vs. Overall]

    * Notifies a Person who hasn't given any negative Dots in a Meeting Section despite the majority of other Participants giving negative feedback.
    * Returns a List of Meeting Section Participants who are Not Perceiving Problems.
    * Returns an empty List if:
        * Fewer than 5 Meeting Section Participants gave Negative Dots
        * Half or fewer of Meeting Section Participants gave Negative Dots
        * All Meeting Section Participants gave Negative Dots
    * This is produced by the following operation(s):
        * Determines whether a majority of Meeting Section Participants gave Negative Dots:
            * Selects Meeting Section Participants who gave Negative Dots.
            * Determines whether more than half of the Meeting Section Participants gave Negative Dots.
        * Determines whether there are at least 5 Meeting Section Participants who gave Negative Dots.
        * Selects Meeting Section Participants who have not given a Negative Dot in the Meeting Section if the two previous conditions are True.
    """
    pass


def question_nubbiness_popup_49(x: objects.Meeting):
    """
    OUTPUT: Question
    INPUT: Responses
    CONTEXT: Meeting
    INSIGHT: Disagreement
    PROCESSING: Context-Only

    * Notifies the Responsible Party and Navigator for a Meeting when a [Question is Nubby](https://blakea-analytics-registry.dev.principled.io/detail?analytic=147) and a [Quorum Exists](https://blakea-analytics-registry.dev.principled.io/detail?analytic=145).
    * Returns a Boolean representing Question Nubbiness Pop-Up.
    """
    pass


def out_of_sync_people_on_question_41(x: objects.Question):
    """
    OUTPUT: Person
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Comparing [Person vs. Believable]

    * Identifies all People who [disagree with](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=167) the [believable choice](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=130) on a Question (if one exists).
    * Returns a list of Out of Sync People on Question.
    * Returns an empty list if there is no Believable Choice or there are no People who disagree with it.
    * This is produced by the following operation(s):
        * Calculates the [Believable Choice](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=130) Response to a Question.
        * Determines whether a Person [disagrees with](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=167) the [Believable Choice](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=130).
        * Selects People for which the condition above is True.
    """
    pass


def split_question_48(x: objects.Question):
    """
    OUTPUT: Person
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Comparing [Collections of People]

    * Determines whether there are two sizable groups of People (each containing >35% of all Responses) whose opinions on a Question are diametrically opposed.
    * Returns a Boolean representing whether a given Question was Split.
    * Returns False if Question Responses are not Scale, Likert, or Yes/No Values.
    * This is produced by the following operation(s):
        * Maps Responses to Summarized Opinions (excludes N/A's).
        * Calculates the counts of Positive Summarized Opinions, Negative Summarized Opinions, and All Summarized Opinions.
        * Calculates the "Positive Ratio" as the ratio of Positive Summarized Opinions and All Summarized Opinions.
        * Calculates the "Negative Ratio" as the ratio of Negative Summarized Opinions and All Summarized Opinions.
        * Determines whether the "Positive Ratio" and the  "Negative Ratio" are both greater than 0.35.
    """
    pass


def team_pair_locking_arms_135(x: objects.Question):
    """
    OUTPUT: Person
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Disagreement
    PROCESSING: Comparing [Collections of People]

    * Identifies whether "Two Teams Are Locking Arms" for a Question when two Teams' managers give different Question Responses and a majority of their respective Teams side with them (>60%).
    * Returns a Boolean representing Team Pair Locking Arms.
    * This is produced by the following operation(s):
        * Determines whether a Team Agrees with their manager:
            * Determines whether a Team has at least 3 People with the same manager.
            * Determines whether more than 60% of the Team gave the same Response as their manager.
        * Determines whether two Teams Agree with their respective managers.
        * Determines whether the two Teams' managers gave different Responses.
    """
    pass


def teams_locking_arms_43(x: objects.Question):
    """
    OUTPUT: Person
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Activity
    PROCESSING: Comparing [Collections of People]

    * Determines whether there is least one [Team Pair is Locking Arms](https://blakea-analytics-registry.dev.principled.io/detail?analytic=135) in Responses to a Question.
    * Returns a Boolean representing Teams Locking Arms.
    * Returns Null if the number of [Team Pair Locking Arms](https://blakea-analytics-registry.dev.principled.io/detail?analytic=135) signals that have not been calculated for every pair of Teams in the Meeting section.
    * This is produced by the following operation(s):
        * Determines whether [Team Pair Locking Arms](https://blakea-analytics-registry.dev.principled.io/detail?analytic=135) signals have been calculated for every pair of Teams in the Meeting Section.
        * Determines whether [Team Pair is Locking Arms](https://blakea-analytics-registry.dev.principled.io/detail?analytic=135) is True for at least one pair of Teams in a Poll Section.
        * Determines whether the two criteria above are both True.
    """
    pass
