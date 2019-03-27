
import copy
import itertools
import numpy as np
from enum import Enum


class Attribute(Enum):
    EMPATHETIC = 'Empathetic'
    CONCEPTUAL = 'Conceptual'
    PRACTICAL = 'Practical'
    WISE = 'Wise'
    SYNTHESIZE = 'Synthesizing the Situation'


class Dot(object):
    def __init__(self, attribute, value, confidence=None):
        assert isinstance(attribute, Attribute), "Must be an Attribute object!"
        self.author = None
        self.subject = None
        self.attribute = attribute
        self.value = value
        self.confidence = confidence


class Meeting(object):
    def __init__(self, title, id):
        self.id = id
        self.title = title
        self.dots = []
        self.questions = []
        self.participants = []

    def add_a_participant(self, person):
        assert isinstance(person, Person), "Must be a Person object!"
        self.participants.append(person)

    def add_a_question(self, question):
        assert isinstance(question, Question), "Must be a Question object!"
        self.questions.append(question)


# TODO: Question Types should be included so responses meet criteria
class Question(object):
    def __init__(self, title, id):
        self.id = id
        self.title = title
        self.responses = {}

    def add_a_response(self, response, responder):
        assert isinstance(response, Response), "Must be a Response object!"
        assert isinstance(responder, Person), "Must be a Person object!"
        self.responses[responder] = response


class ResponseType(Enum):
    RIGHT = 'Correct'
    WRONG = 'Incorrect'


class Response(object):
    def __init__(self, text, id, response_type=ResponseType.RIGHT):
        self.id = id
        self.text = text
        self.response_type = response_type


class Person(object):
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.historical_dots = []

    def give_dot(self, dot, subject, meeting=None):
        assert isinstance(dot, Dot), "Dot must be a Dot object!"
        assert isinstance(subject, Person), "Subject must be a Person object!"

        dot = copy.copy(dot)

        dot.author = self
        dot.subject = subject
        subject.historical_dots.append(dot)

        if meeting:
            meeting.dots.append(dot)

    @property
    def bbc(self):
        bbc = {}
        sorted_dots = sorted(self.historical_dots, key=lambda x: x.attribute.value)
        for attribute, dots in itertools.groupby(sorted_dots, lambda x: x.attribute.value):
            bbc[attribute] = np.average([i.value for i in dots])

        return bbc


class PopUp(object):
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def activate(self):
        return 1
