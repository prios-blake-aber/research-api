
from src import meta
from enum import Enum


class NumericRange(Enum):
    """
    Enumeration that fixes the range of numerical values.
    """
    ONE_TO_TEN = 1
    ONE_TO_FIVE = 2
    ONE_TO_THREE = 3


class QuestionType(Enum):
    """Stub for the possible enumerations of Question Type"""
    LIKERT = 'Likert'
    SCALE = 'Scale'
    CATEGORICAL = 'Categorical'
    BINARY = 'Binary'


class Judgement(meta.Assertion):
    """Judgement"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Comparison(meta.Assertion):
    """Comparison"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Dot(Judgement):
    """Dot"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Ranking(Judgement):
    """Ranking"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Response(Judgement):
    """Response"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AssertionSet(meta.Entity):
    """AssertionSet (Useful for Logic"""
    def __init__(self, **kwargs):
        _allowable_collections = {'members': meta.Assertion}
        super().__init__(allowable_collections=_allowable_collections, **kwargs)


class CollectionOfScaleValues(AssertionSet):
    """AssertionSet (Useful for Logic"""
    def __init__(self, **kwargs):
        _allowable_collections = {'members': meta.Assertion}
        super().__init__(allowable_collections=_allowable_collections, **kwargs)


class DotCollection(CollectionOfScaleValues):
    """Collection of Dots"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ResponseCollection(AssertionSet):
    """Collection of Responses"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RelevanceCollection(AssertionSet):
    """Collection of Relevance Scores"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Question(meta.Entity):
    """Question"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'title', 'description', 'question_type'}
        _allowable_collections = {'responses': Response}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)


class Attribute(meta.Entity):
    """Attribute"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'name', 'description'}
        _allowable_collections = {'members': Attribute}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)


class RelevanceScore(meta.Assertion):
    """RelevanceScore"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_value(self, value):
        if value not in range(0, 1):
            raise ValueError('rating must be a float from 0 to 1')



class BooleanOption(meta.Assertion):
    """BooleanOption"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_value(self, value):
        if (not isinstance(value, bool)) or not None:
            raise ValueError('Output type must be Boolean or None')


class FloatOption(meta.Assertion):
    """FloatOption"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_value(self, value):
        if (not isinstance(value, float)) or not None:
            raise ValueError('Output type must be Float or None')


class StringOption(meta.Assertion):
    """StringOption"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_value(self, value):
        if (not isinstance(value, str)) or not None:
            raise ValueError('Output type must be String or None')


class System(meta.Entity):
    """System"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Person(meta.Entity):
    """Person"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'name', 'role', 'description', 'believability'}
        _allowable_collections = {'dots': Dot}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)


class Team(meta.Entity):
    """Team"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'name', 'description'}
        _allowable_collections = {'members': Person}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)


class Meeting(meta.Entity):
    """Meeting"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'name', 'description'}
        _allowable_collections = {'dots': Dot, 'questions': Question, 'participants': Person}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)