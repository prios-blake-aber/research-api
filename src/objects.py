
from enum import Enum


class QuestionType(Enum):
    """Stub for the possible enumerations of Question Type"""
    LIKERT = 'Likert'
    SCALE = 'Scale'
    CATEGORICAL = 'Categorical'
    BINARY = 'Binary'


class EntityCollection(object):
    """A collection of Entity objects sharing the same type
        1) Used to instantiate container-like attributes in an Entity
        2) Type checks all elements of the container
        3) Has append() method to add new elements to container
    """
    def __init__(self, list_of_entities):
        assert isinstance(list_of_entities, list), "Must be a list!"
        self.type = type('NotSet', (object,), {})
        self.check_consistent_types(list_of_entities)
        self.data = list_of_entities

    def __repr__(self):
        return '{n} members of type {t}'.format(n=len(self.data), t=self.type.__name__)

    def check_consistent_types(self, list_of_entities):
        """Records the type of the first appended item and detects inconsistency"""
        if list_of_entities:
            assert len(set(type(i) for i in list_of_entities)) == 1, "Entities must share common type!"
            self.type = type(list_of_entities.pop())

    def append(self, item):
        """Appends new items to container, records expected type, checks type consistency"""
        if not self.data:
            self.type = type(item)
        else:
            assert isinstance(item, self.type), "Entities must be of type {t}!".format(t=self.type)
        self.data.append(item)


class Entity(object):
    """A generic Entity object with attributes, containers and dynamically generated methods
        1) Attributes can be defined on instantiation via kwargs
        2) Container attributes have special functionality
            a) Instantiates with a list
            b) Generates a special method that appends to this list
        3) This class is expected to act as a MixIn for Domain Objects
    """
    def __init__(self, allowable_attributes=None, allowable_collections=None, **kwargs):
        defined_attributes = set(kwargs.keys())
        expected_attributes = set(allowable_attributes)
        expected_collections = set(allowable_collections.keys())

        for kw in expected_attributes.union(defined_attributes).difference(expected_collections):
            if kw not in expected_attributes.difference(defined_attributes):
                setattr(self, kw, kwargs[kw])
            else:
                setattr(self, kw, None)

        for kw in expected_collections:
            if kw in defined_attributes:
                self._add_collection(kw, kwargs[kw])
            else:
                self._add_collection(kw)
            self._instantiate_collection_functions(kw, allowable_collections)

    def _add_collection(self, attribute, list_of_entities=None):
        """Add a new collection as an attribute (Not recommended for ad hoc use)"""
        if list_of_entities:
            entities = EntityCollection(list_of_entities)
        else:
            entities = EntityCollection([])

        setattr(self, attribute, entities)

    def _add_to_a_collection(self, item, attribute, expected_object):
        """Append new items to an existing collection (Not recommended for ad hoc use)"""
        assert expected_object, "Attribute {a} does not allow this object!".format(a=attribute)
        assert isinstance(item, expected_object), "Must be a {t} object!".format(t=type(expected_object))
        list_of_items = getattr(self, attribute)
        list_of_items.append(item)

    def _instantiate_collection_functions(self, attribute, allowable_collections):
        """Adds a method for each defined collection on instantiation (Not recommended for ad hoc use)"""
        object_type = allowable_collections.get(attribute)

        def add_function(x):
            return self._add_to_a_collection(x, attribute, object_type)

        add_function.__name__ = 'add_{x}'.format(x=attribute)
        add_function.__doc__ = 'Adds {o} objects to the "{a}" collection'.format(
            o=object_type.__name__, a=attribute
        )

        setattr(self, add_function.__name__, add_function)


class Assertion(object):
    """A generic Assertion object
        1) The "source" and "target" attributes should both be an Entity
        2) The "value" should be some numerical value
        3) The "confidence" should be some numerical value
        4) The "description" should be a free-form text field
        5) The "measure" should be the Entity ascribing semantic meaning to the "value"
        6) The "context" should be a list of Tags, Entities, etc that contextualize assertions
    """
    def __init__(self, source, target, value, measure=None, context=None, description=None, confidence=None):
        self.source = source
        self.target = target
        self.value = value
        self.measure = measure
        self.context = context
        self.description = description
        self.confidence = confidence


class Dot(Assertion):
    """Dot"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Ranking(Assertion):
    """Ranking"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Response(Assertion):
    """Response"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Question(Entity):
    """Question"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'title', 'description', 'question_type'}
        _allowable_collections = {'responses': Response}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)


class Attribute(Entity):
    """Attribute"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'name', 'description'}
        _allowable_collections = {'members': Attribute}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)


class Person(Entity):
    """Person"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'name', 'role', 'description'}
        _allowable_collections = {'dots': Dot}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)


class Team(Entity):
    """Team"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'name', 'description'}
        _allowable_collections = {'members': Person}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)


class Meeting(Entity):
    """Meeting"""
    def __init__(self, **kwargs):
        _allowable_attributes = {'name', 'description'}
        _allowable_collections = {'dots': Dot, 'questions': Question, 'participants': Person}
        super().__init__(_allowable_attributes, _allowable_collections, **kwargs)
