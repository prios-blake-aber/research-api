
"""
Polarization:
"""

from typing import List, TypeVar
from prios_api.src import foundation
from prios_api.domain_objects import objects

StringOrFloat = TypeVar("StringOrFloat", str, float)
_THRESHOLD_HIGH = 1.7
_THRESHOLD_STD_SCALE = 1.0
_THRESHOLD_STD_MAPPED_SCALE = 0.5
_THRESHOLD_POLES = 0.25
_MINIMUM_THRESH = 0.7


def polarizing_stat(values: List[float]) -> float:
    """
    Returns the polarization statistic, which measures the balance between positive opinions and
    negative opinions.

    It is the minimum of ratio of the number of positive
    opinions to the number of negative opinions and the ratio of the number of negative opinions
    to the number of positive opinions.

    Parameters
    ----------
    values
        List of values

    Returns
    -------
    float
        Polarization statistic.
    """
    mapped_values = [foundation.map_values(vi, objects.NumericRange.ONE_TO_TEN) for vi in values]

    def negative_sentiment(x):
        return x == 1

    def positive_sentiment(x):
        return x == 3

    percent_negative = foundation.percent_satisfying_condition(mapped_values, negative_sentiment)
    percent_positive = foundation.percent_satisfying_condition(mapped_values, positive_sentiment)

    if percent_negative > 0 and percent_positive > 0:
        return min(percent_positive/percent_negative, percent_negative/percent_positive)
    else:
        return 0


def is_polarizing(values: List[float],
                  thresh_on_std_scale: float = _THRESHOLD_STD_SCALE,
                  thresh_on_std_mapped_scale: float = _THRESHOLD_STD_MAPPED_SCALE,
                  thresh_on_poles: float = _THRESHOLD_POLES) -> bool:
    """
    "Is polarizing" is a predicate on a distribution of values on the 1-to-10 scale. It returns
    True if the distribution satisfies three criteria:
    * Divisiveness statistic (after mapping to sentiment) exceeds `thresh_on_std_mapped_scale`
    * Divisiveness statistic (raw values) exceeds `thresh_on_std_scale`
    * Polarization statistic exceeds `thresh_on_poles`

    Parameters
    ----------
    values
    thresh_on_std_scale
    thresh_on_std_mapped_scale
    thresh_on_poles

    Returns
    -------
    bool
        True if the distribution of values satisfies three sets of criteria.
    """
    polarization = polarizing_stat(values) > thresh_on_poles
    divisiveness = divisiveness_stat(values) > thresh_on_std_mapped_scale
    std_dev = divisiveness_stat(values, map_to_sentiment=False) > thresh_on_std_scale
    return polarization and divisiveness and std_dev


def is_polarizing_v0(scale_assertions: objects.ScaleValueSet,
                     thresh_on_std_scale: float = _THRESHOLD_STD_SCALE,
                     thresh_on_std_mapped_scale: float = _THRESHOLD_STD_MAPPED_SCALE,
                     thresh_on_poles: float = _THRESHOLD_POLES) -> objects.Judgement:
    """
    Is polarizing

    Parameters
    ----------
    scale_assertions
        List of assertions with scale values.
    thresh_on_std_scale
        Threshold on standard deviation of scale values.
    thresh_on_std_mapped_scale
        Threshold on standard deviation of scale values mapped to 1, 2, and 3
    thresh_on_poles
        Threshold on ratio between poles

    Returns
    -------
    object.Judgement
        Whether a set of scale values are polarizing.
    """
    values = [xi.value for xi in scale_assertions.data]
    mapped_values = [foundation.map_values(vi, objects.NumericRange.ONE_TO_TEN) for vi in values]

    # TODO: nesting functions here is terrible; why not use the sentiment module?
    def negative_sentiment(x):
        return x == 1

    def positive_sentiment(x):
        return x == 3

    percent_negative = foundation.percent_satisfying_condition(mapped_values, negative_sentiment)
    percent_positive = foundation.percent_satisfying_condition(mapped_values, positive_sentiment)

    if percent_negative > 0 and percent_positive > 0:
        pole_ratio = min(percent_positive/percent_negative, percent_negative/percent_positive)
    else:
        pole_ratio = 0

    std_values_condition = foundation.standard_deviation(values) > thresh_on_std_scale
    std_mapped_values_condition = foundation.standard_deviation(mapped_values) > thresh_on_std_mapped_scale
    pole_condition = pole_ratio > thresh_on_poles
    result = std_values_condition and std_mapped_values_condition and pole_condition
    return objects.Judgement(source=objects.System, target=objects.System, value=result)


