
"""
TBD
"""

from prios_api.domain_objects import meta
from dataclasses import dataclass, field
import typing
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
    RATING = 'Rate This Section'


class MeetingNubbyClassification(Enum):
    # TODO: Generalize Classification Class.
    NOT_NUBBY = 1
    LESS_NUBBY = 2
    SOMEWHAT_NUBBY = 3
    NUBBY = 4
    VERY_NUBBY = 5


@dataclass
class Judgement(meta.Assertion):
    description: typing.Optional[str] = 'A Judgement made by one Entity about another Entity'


@dataclass
class Comparison(meta.Assertion):
    description: typing.Optional[str] = 'A Comparison made between two Entities'


@dataclass
class Dot(Judgement):
    description: typing.Optional[str] = None


@dataclass
class Person(meta.Entity):
    name: typing.Optional[str] = None
    role: typing.Optional[str] = None
    description: typing.Optional[str] = None
    believability: typing.Optional[float] = 0.01
    dots: typing.List[Dot] = field(default_factory=list)


@dataclass
class Team(meta.Entity):
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None


@dataclass
class Ranking(Judgement):
    description: typing.Optional[str] = None


@dataclass
class Response(Judgement):
    # TODO: Is this an artifact?
    source: typing.Optional[Person] = None
    description: typing.Optional[str] = None


@dataclass
class Question(meta.Entity):
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    question_type: typing.Optional[QuestionType] = None
    responses: typing.List[Response] = field(default_factory=list)


@dataclass
class Meeting(meta.Entity):
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    dots: typing.List[Dot] = field(default_factory=list)
    questions: typing.List[Question] = field(default_factory=list)
    participants: typing.List[Person] = field(default_factory=list)
