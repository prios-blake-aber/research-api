
from src import objects


def dots_aggregation_5(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Estimates a Person's score on an Attribute based on the average of their Dots received on that Attribute.

    * Returns a list including a Scale Value representing a Person's Dots Aggregation score and an integer representing the total number of Dots a Person has received.

    * Returns Null if the Person has received fewer than 10 Dots.

    * This is produced by the following operation(s):
       * Determines if the Person has received at least 10 Dots on an Attribute.

       * Calculates the count of Dots a Person has received on that Attribute.

       * Calculates the average of all Dots that Attribute if the previous condition is True.
    """
    pass


def dots_aggregation_5(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Dots
    CONTEXT: AssertionSet
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Estimates the probable lower bound of a Person's Dots score, taking into account both the score of Dots received as well as the number.
    * Returns a Statistic between 0-1 that represents the minimum fraction of positive ratings a Person has received with 95% confidence, or, a Person's Lower Bound [Wilson Score](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval).
    * This is produced by the following operation(s):
        * Determines whether a Person has received at least one Dot on an Attribute.
        * Calculates the lower bound Wilson Score if the previous condition was True.
    """
    pass


def ranking_aggregation_9(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Rankings
    CONTEXT: AssertionSet
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Estimates a Person's score on an Attribute based on the average of their Rankings received on that Attribute.
    * Returns a list including a Scale Value representing a Ranking Aggregation score and an integer representing the number of Rankings a Person has received.
    * Returns Null if a Person has fewer than 10 Rankings.
    * This is produced by the following operation(s):
        * Determines if a Person has at least 10 Rankings.
        * Calculates the count of Rankings a Person has received on that Attribute.
        * Calculates the average of all Rankings if the previous condition is True.
    """
    pass


def all_stream_1(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: Streams
    CONTEXT: AssertionSet
    INSIGHT: Synthesis
    PROCESSING: Context-Only

    * Estimates a Person's score on an Attribute based on the average of scores for that Attribute for the Streams (Dots Aggregation, Tests, and Ranking Aggregation) on which they have a value.
    * Returns a list representing the number of entity events on the Attribute and a Person’s All Stream Score.
    * Returns Null if a Person does not have scores for any of the Streams (Dots Aggregation, Tests, and Ranking Aggregation).
    * This is produced by the following operation(s):
        * Calculates the sum of the entity events (individual Dots, Rankings, and Test Score) that comprise the Dot Aggregation, Ranking Aggregation, and Tests Streams on the Attribute.
        * Calculates the average of a Person's scores on Dots Aggregation, Tests, and Ranking Aggregation excluding Streams on which a Person does not have a score.
    """
    pass


def attribute_believability_193(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: All-Stream
    CONTEXT: AssertionSet
    INSIGHT: Believability
    PROCESSING: Context-Only

    * Defines "Attribute Believability" as the weight a Person's opinion should receive, relative to others, on matters pertaining to that Attribute based on their All Stream score for that Attribute.

    * Returns a number from 0-1 representing Attribute Believability.

    * Returns Null if the Person does not have an [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) score on the Attribute.

    * This is produced by the following operation(s):
       * Maps the Person's [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) score on the Attribute to a score between 0-1.
       * Calculates the square of the result from the previous step which represents the Person's Attribute Believability weight.
    """
    pass


def attribute_believability_193(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: All-Stream
    CONTEXT: AssertionSet
    INSIGHT: Believability
    PROCESSING: Context-Only

    * Defines "Attribute Believability" as the weight a Person's opinion should receive, relative to others, on matters pertaining to that Attribute based on their All Stream score for that Attribute.

    * Returns a number from 0-1 representing Attribute Believability.

    * Returns Null if the Person does not have an [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) score on the Attribute.

    * This is produced by the following operation(s):
       * Determines whether the Person has at least 10 events (individual Dots, Rankings, and Test Scores) on the Attribute.
       * Maps the Person's [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) score on the Attribute to a score between 0-1 if the previous condition was True.
       * Calculates the square of the result from the previous step which represents the Person's Attribute Believability weight.
    """
    pass


def general_believability_192(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: All-Stream
    CONTEXT: AssertionSet
    INSIGHT: Believability
    PROCESSING: Context-Only

    * Defines "General Believability" as the weight a Person's opinion should receive on general matters based on their [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) scores for a selected set of Attributes.

    * Returns a Statistic, a number from 0-1, that represents General Believability.

    * Returns Null if a Person has no All Stream score for any of the Attributes the client has configured to contribute to General Believability (client configuration information can be found [in the appendix](https://docs.google.com/document/d/1RafxVjqFCjkOLLx7cClbRsJLIuOjxSY2zvKuK-A_qgE/edit#heading=h.hj4e45f2b8hb)).

    * This is produced by the following operation(s):
      * Maps the Person's [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) scores on the Attributes to scores between 0-1.

      * Determines whether the Person has a score on at least one Attribute that contributes to General Believability.

      * Calculates a weighted average of the All Stream scores with weights specified by clients for how much an Attribute should contribute to General Believability. If weights are unspecified, defaults to an equal-weighted average. If an Attribute does not have an All Stream score, it is excluded from the average.

      * Calculates the square of the previous step.
    """
    pass


def general_believability_192(x: objects.AssertionSet):
    """
    OUTPUT: AssertionSet
    INPUT: All-Stream
    CONTEXT: AssertionSet
    INSIGHT: Believability
    PROCESSING: Context-Only

    * Defines "General Believability" as the weight a Person's opinion should receive on general matters based on their [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) scores for a selected set of Attributes.

    * Returns a Statistic, a number from 0-1, that represents General Believability.

    * Returns Null if a Person has no All Stream score for any of the Attributes the client has configured to contribute to General Believability (client configuration information can be found [in the appendix](https://docs.google.com/document/d/1RafxVjqFCjkOLLx7cClbRsJLIuOjxSY2zvKuK-A_qgE/edit#heading=h.hj4e45f2b8hb)) or if the Person does not have at least 10 events total between Dots, Rankings, and Tests on the Attributes that contribute to General Believability.

    * This is produced by the following operation(s):
      * Maps the Person's [All Stream](https://blakea-analytics-registry.dev.principled.io/writeup?analytic=1) scores on the Attributes to scores between 0-1.

      * Determines whether the Person has a score on at least one Attribute that contributes to General Believability.

      * Determines whether the Person has at least 10 events (individual Dots, Rankings, and Test Scores) on the Attributes that contribute to General Believability.

      * Calculates a weighted average of the All Stream scores with weights specified by clients for how much an Attribute should contribute to General Believability if the previous two conditions were true. If weights are unspecified, defaults to an equal-weighted average. If an Attribute does not have an All Stream score, it is excluded from the average.

      * Calculates the square of the previous step.
    """
    pass
