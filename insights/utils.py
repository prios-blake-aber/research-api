
from src import objects


def dot_count_26(x: objects.Meeting):
    """
    OUTPUT: Statistics
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Grouping
    PROCESSING: Comparing [Believable vs. Overall]

    * Calculates Dot counts based on whether they are Positive, Neutral, or Negative, using both equal- and Believability-weighting for all Dots received or all Dots received in a Meeting dependent on the context in which it is called.
    * Returns a List containing two of each of the following Statistics, which are calculated using two sets of weights: equal weights and Author Believability.
      * Count and Believability-adjusted count for Positive Dots.
      * Count and Believability-adjusted count for Neutral Dots.
      * Count and Believability-adjusted count for Negative Dots.
      * Count and Believability-adjusted count for all Dots.
    * Returns Null if a Person has received no Dots.
    * This is produced by the following operation(s):
        * Calculates and returns the count of Dots and Believability-adjusted count of Dots for Dots given to the Subject that:
          * Equal or exceeds the Positive threshold (6.5, which is non-standard).
          * Exceed the Negative threshold (5.5, which is non-standard) and are less than the Positive threshold (6.5, which is non-standard).
          * Equal or are less than the Negative threshold (5.5, which is non-standard).
        * Calculates the total Believability-adjusted count of Dots which represents a Person's Believability-Weighted Dot Count.
        * Calculates the total count of all Dots a Person has received which represents a Person's equally-weighted Dot Count.
    """
    pass


def dots_summary_186(x: objects.AssertionSet):
    """
    OUTPUT: Person
    INPUT: nan
    CONTEXT: Dots
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Defines the Dots Summary as either a Believability and Author Capped Dots Summary with weights as the product of the [Capped Author Weights](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=171) and Author's [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16) weights or as the Author-Capped Dots Summary with weights as the [Capped Author Weights](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=171).
    * Returns a Scale Value representing the (Believable) Dots Summary.
    * Returns Null if there are no Dots.
    * This is produced by the following operation(s):
        * Calculates the [Capped Author Weights](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=171) for each Author.
        * If calculating the Believable Dots Summary, multiplies each weight by the Author's Believability, or 0.01 if the Author doesn't have a Believability.
        * Calculates the weighted average of the Dot values, using the previously calculated weights.
    """
    pass


def dot_matrix_51(x: objects.AssertionSet):
    """
    OUTPUT: Statistics
    INPUT: Dots
    CONTEXT: Dots
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Defines each Author’s overall view of each Subject as either the average of all Dots given or the Author's Desired Synthesis.
    * Returns a Dictionary mapping Author-Subject pairs to Scale Values representing the Dot Matrix.
    * This is produced by the following operation(s):
        * Calculates each Author's Implied Synthesis of each Subject: Calculates the average Dot rating given by each Author to each Subject.
        * Selects the Author's Desired Synthesis if provided, otherwise selects the Author's Implied Synthesis.
    """
    pass

def dot_matrix_entry_150(x: objects.AssertionSet):
    """
    OUTPUT: Statistics
    INPUT: Dots
    CONTEXT: Dots
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Defines an Author’s view of each Subject as either the average of Dots given or the Author's desired synthesis, if provided.
    * Returns a dictionary for a Subject-Author Pair containing:
       * A Statistic representing the count of Dots given from Author to Subject.
       * A Scale Value representing the Author's view of the Subject, i.e. their Implied Synthesis.
       * And, if it exists, a Scale Value that represents an Author's Desired Synthesis view of the Subject.
    * This is produced by the following operation(s):
        * Calculates the count of Dots given by an Author to a Subject.
        * Calculates the Author's Implied Synthesis of the Subject: Calculates the average Dot rating given by the Author to the Subject.
        * Selects the Author's Desired Synthesis if provided, otherwise selects the Author's Implied Synthesis.
    """
    pass


def global_dot_statistics_133(x: objects.AssertionSet):
    """
    OUTPUT: Statistics
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Aggregates the results of several other analytics: [Dot Count](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=32), [Global/Meeting Dot Average](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=26), [Dot Score Relative to the Population](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=27), and [Wilson Score](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=8) calculated for all Dots a Person has received.
    * Returns a dictionary of:
       * a Person's [Dot Count](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=32) on all Dots received
       * a Person's [Global/Meeting Dot Average](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=26) on all Dots received
       * a Person's [Dot Score Relative to the Population](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=27) on all Dots received
       * a Person's Lower Bound [Wilson Score](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=8) on all Dots received
    * Returns an empty dictionary if a Person has received no Dots
    * This is produced by the following operation(s):
        * Combines the results of all of the analytics mentioned above into a dictionary.
    """
    pass


def global_dot_average_32(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Estimates a Person's score on an Attribute based on the equal- and Believability-weighted average of all Dots received or all Dots received in Meetings depending on the context in which it was called.
    * Returns a Scale Value representing a Person's Global/Meeting Dot Average.
    * Returns Null if a Person has not received any Dots.
    * This is produced by the following operation(s):
        * Determines if a Person has received at least 1 Dot.
        * Determines if the Dots a Person has received have corresponding Believability weights from the authors.
        * Calculates the weighted average of all Dots received if the previous condition is True.
        * Calculates the equal average of all Dots received if the previous condition was False.
    """
    pass


def response_summary_139(x: objects.Question):
    """
    OUTPUT: Response
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Normalization
    PROCESSING: Comparing [Believable vs. Overall]

    * Calculates the Question Response percentages at each answer choice with equal- and Believability-weighting. For Contribution or Force Ranking Questions, calculates the average Author rating for each Person with equal- and Believability-weighting.
    * Returns a Question Response Summary which contains a set of counts by Histogram bucket or the average and Believability-weighted average of the answers, depending on Question type.
    * Returns Null if no one has answered the Question and returns Null for the Believability-weighted Average if no one Believable answered the Question (if the sum of Believability of Question Respondents equals 0).
    * This is produced by the following operation(s):
        * For Likert, One-to-Ten, and Categorical questions, calculates the histogram and the Believability-weighted average Response for each answer choice.
        * For Relative Contribution and Force Ranking Questions, calculates the average Response per Subject and Believability-weighted average Response per Subject.
    """
    pass


def dot_meeting_statistics_132(x: objects.Meeting):
    """
    OUTPUT: Statistics
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Synthesis
    PROCESSING: Composite

    * Aggregates the results of several other analytics: [Dot Count](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=32), [Global/Meeting Dot Average](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=26), [Dot Score Relative to the Population](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=27), and [Wilson Score](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=8) calculated for all Dots the Person has received in Meetings.
    * Returns a dictionary of:
       * a Person's [Dot Count](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=32) on all Dots received in Meetings
       * a Person's [Global/Meeting Dot Average](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=26) on all Dots received in Meetings
       * a Person's [Dot Score Relative to the Population](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=27) on all Dots received in Meetings
       * a Person's Lower Bound [Wilson Score](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=8) on all Dots received in Meetings
    * Returns an empty dictionary if a Person has received no Dots in Meetings
    * This is produced by the following operation(s):
        * Combines the results of all of the analytics mentioned above into a dictionary.
    """
    pass


def stream_population_summary_140(x: objects.AssertionSet):
    """
    OUTPUT: Streams
    INPUT: Streams
    CONTEXT: AssertionSet
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Aggregates the Count, Average, Variance, and Cumulative Distribution for several other analytics: [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1), [Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=14), [General Believability](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=16), [Dot Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=5), [Ranking](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=9) and [Tests](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=13) of Stream Values into a Population Summary.
    * Returns a Map of population statistics (i.e. size, average, variance, Cumulative Distribution) for each Stream
    * Returns empty elements in a Population Summary in cases where input data for an individual Stream is Null
    * This is produced by the following operation(s):
        * Calculates the following statistics to calculate the Cumulative Distribution:
         * Calculates a list of strictly increasing values
         * Calculates a list of the corresponding proportions of values less than or equal to that value
        * Maps the Count, Average, Variance, and Cumulative Distribution of each stream into a list of Population Summaries
    """
    pass


def strongest_all_stream_attributes_28(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: All-Stream
    CONTEXT: AssertionSet
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Selects up to 3 highest rated Attributes for one Person from those with an [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) score of 7 or more.
    * Returns a List of up to 3 Attributes representing a Person's Strongest All Stream Attributes.
    * Returns an empty List if a Person does not have any Attributes with All Stream scores with a score equal or greater than the Positive Threshold (7).
    * This is produced by the following operation(s):
        * Determines if any of a Person's All Stream scores meet or surpass the Positive Threshold.
        * Selects the highest rated 3 Attributes from a sorted list of Attributes from the previous step.
    """
    pass


def weakest_all_stream_attributes_29(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: All-Stream
    CONTEXT: AssertionSet
    INSIGHT: Sentiment
    PROCESSING: Context-Only

    * Selects up to 3 lowest rated Attributes for a Person from those with an [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) rating of 4.5 or less.
    * Returns a List of up to 3 Attributes representing a Person's Weakest All Stream Attributes.
    * Returns an empty list if a Person does not have any Attributes with All Stream scores with a score less than or equal to the Negative Threshold (4.5, which is non-standard).
    * This is produced by the following operation(s):
        * Determines if any of a Person's All Stream scores meet or are lower than the Negative Threshold (4.5, which is non-standard).
        * Selects up to 3 of the lowest rated Attributes from a sorted list of Attributes from the previous step.
    """
    pass


def group_by_question_response_168(x: objects.Question):
    """
    OUTPUT: Person
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Grouping
    PROCESSING: Context-Only

    * Classifies People into groups based on their Question Responses.
    * Returns:
      * For Scale and Likert Question Types: A map of People to Summarized Opinions that represents Factions.
      * For Yes/No Question Types: A map of People to Yes/No Values that represents Factions.
      * For Categorical Question Types: A map of People to their Responses.
    * This is produced by the following operation(s):
        * Maps People to Summarized Opinions (for Scale and Likert Questions), Yes / No Values (for Yes/No Questions, or their original Responses (for Categorical Questions) based on their Question Responses.
    """
    pass


def relative_contribution_rescaling_52(x: objects.Question):
    """
    OUTPUT: Person
    INPUT: Responses
    CONTEXT: Question
    INSIGHT: Normalization
    PROCESSING: Context-Only

    * Rescales an Author's Response to a relative contribution Question to ensure that their positive contributions for all Subjects sum to 100% and their negatives to -5%.
    * Returns a dictionary of People with a corresponding number that represents a Person's Relative Contribution to a Meeting Section and is between -5 and 100.
    * This is produced by the following operation(s):
        * Determines if a Contribution Question response is Negative (less than 0) or Positive (greater than or equal to 0).
        * Calculates the sums of Responses classified as Negative and Positive.
        * Calculates the Negative Scaling and Positive Scaling Factors, respectively, by dividing the maximum negative threshold (-5) by the sum of Negative Responses, and the maximum positive threshold (100) by the sum of Positive Responses.
        * Maps the Negative Scaling and Positive Scaling Factors to each Rating on a subject.
    """
    pass


def dot_score_relative_to_population_27(x: objects.Meeting):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: Meeting
    INSIGHT: Synthesis
    PROCESSING: Comparing [Person vs. Overall]

    * Calculates a statistic representing how a Person's Dots on an Attribute compares to the overall group’s Performance on the same Attribute (currently assumed to be 5) on all Dots received or all Dots received in Meetings dependent on the context in which it was called.
    * Returns a Statistic from negative infinity to positive infinity which represents a Person's Dot Score Relative to the Population.
    * Returns Null if a Person has not received any Dots.
    * This is produced by the following operation(s):
        * Calculates the sum of the Ratings for all of the Dots a Person has received.
        * Calculates the product of the NetScoreOffset (assumed average score of 5) and the number of Dots a Person has received.
        * Calculates Dot Score Relative to the Population by subtracting the results of the previous two steps.
    """
    pass


def capped_author_weights_171(x: objects.AssertionSet):
    """
    OUTPUT: Assertion
    INPUT: AssertionSet
    CONTEXT: AssertionSet
    INSIGHT: Normalization
    PROCESSING: Context-Only

    * Calculates weights to apply to [cap](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=173) all observations from a particular Author, based on a set of Dots.
    * Returns a Statistic between 0 and 1 representing the Capped Author Weight.
    * This is produced by the following operation(s):
        * Calculates a count of the Dots by the Author.
        * Calculates a [Capped Weight](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=173) based on the count.
    """
    pass


def capping_173(x: objects.AssertionSet):
    """
    OUTPUT: Assertion
    INPUT: AssertionSet
    CONTEXT: AssertionSet
    INSIGHT: Normalization
    PROCESSING: Context-Only

    * Defines the Capped Weight as the weight given each observation by a single label from a set of labeled observations, based on a parameterized asymptotic upper bound on the maximum impact any label can have, denominated in terms of number of observations.
    * Returns a Statistic between 0 and 1 representing a Capped Weight.
    * This is produced by the following operation(s):
        * Calculates (counts) the number of observations associated with the particular label.
        * Calculates the Capped Weight by applying an asymptotic capping function to the number of observations. The Capped Weight is always equal to 1 when there's one observation, and as the number of observations N increases beyond the upper bound, the Capped Weight converges to approximately 1 / N.
    """
    pass
