
from enum import Enum


class QuestionType(Enum):
    LIKERT = 'Likert'
    SCALE = 'Scale'
    CATEGORICAL = 'Categorical'
    BINARY = 'Binary'


class EntityCollection(object):
    def __init__(self, list_of_entities):
        assert isinstance(list_of_entities, list), "Must be a list!"
        self.type = None
        self.check_consistent_types(list_of_entities)
        self.data = list_of_entities

    def check_consistent_types(self, list_of_entities):
        if list_of_entities:
            assert len(set(type(i) for i in list_of_entities)) == 1, "Entities must share common type!"
            self.type = type(list_of_entities.pop())

    def append(self, item):
        if self.type:
            assert isinstance(item, self.type), "Entities must be of type {t}!".format(t=self.type)
        self.data.append(item)


class Entity(object):
    def __init__(self, allowable_attributes=None, allowable_collections=None, **kwargs):
        input_attributes = set(kwargs.keys())
        expected_attributes = set(allowable_attributes).union(set(kwargs.keys()))
        attributes_to_populate = input_attributes.intersection(allowed_attributes)
        attributes_to_default = allowed_attributes.difference(input_attributes)
        for attribute in attributes_to_populate:
            if key in allowable_attributes:
                setattr(self, key, value)
            if key in allowable_collections:
                self._add_collection(key, value)
                self._instantiate_collection_functions(key, allowable_collections)


            if key in allowable_attributes:
                setattr(self, key, value)
            if key in allowable_collections:
                self._add_collection(key, value)
                self._instantiate_collection_functions(key, allowable_collections)


    def _add_collection(self, attribute, list_of_entities=None):
        if list_of_entities:
            entities = EntityCollection(list_of_entities)
        else:
            entities = EntityCollection([])

        setattr(self, attribute, entities)

    def _add_to_a_collection(self, item, attribute, expected_object):
        assert expected_object, "Attribute {a} does not allow this object!".format(a=attribute)
        assert isinstance(item, expected_object), "Must be a {t} object!".format(t=type(expected_object))
        list_of_items = getattr(self, attribute)
        list_of_items.append(item)

    def _instantiate_collection_functions(self, attribute, allowable_collections):
        object_type = allowable_collections.get(attribute)

        def add_function(x):
            return self._add_to_a_collection(x, attribute, object_type)

        add_function.__name__ = 'add_{x}'.format(x=attribute)
        add_function.__doc__ = 'Adds {o} objects to the "{a}" collection'.format(
            o=object_type.__name__, a=attribute
        )

        setattr(self, add_function.__name__, add_function)


class Assertion(object):
    def __init__(self, source, target, measure, value, context=None, confidence=None):
        self.source = source
        self.target = target
        self.context = context
        self.measure = measure
        self.value = value
        self.confidence = confidence


class Dot(Assertion):
    def __init__(self, *args):
        super().__init__(*args)


class Ranking(Assertion):
    def __init__(self, *args):
        super().__init__(*args)


class Response(Assertion):
    def __init__(self, *args):
        super().__init__(*args)


class Question(Entity):

    _allowable_attributes = {'title', 'description', 'question_type'}
    _allowable_collections = {'responses': Response}

    def __init__(self, **kwargs):
        super().__init__(self._allowable_attributes, self._allowable_collections, **kwargs)


class Attribute(Entity):
    _allowable_attributes = {'name', 'description'}

    def __init__(self, **kwargs):
        super().__init__(self._allowable_attributes, **kwargs)


class Person(Entity):
    _allowable_attributes = {'name', 'role', 'description'}
    _allowable_collections = {'dots': Dot}

    def __init__(self, **kwargs):
        super().__init__(self._allowable_attributes, self._allowable_collections, **kwargs)


class Team(Entity):
    _allowable_attributes = {'name', 'description'}
    _allowable_collections = {
        'members': Person
    }

    def __init__(self, **kwargs):
        super().__init__(self._allowable_attributes, self._allowable_collections, **kwargs)


class Meeting(Entity):
    _allowable_attributes = {'name', 'description'}
    _allowable_collections = {
        'dots': Dot, 'questions': Question, 'participants': Person
    }

    def __init__(self, **kwargs):
        super().__init__(self._allowable_attributes, self._allowable_collections, **kwargs)
