
"""
TBD
"""

import time


class EntityCollection(object):
    """A collection of Entity objects sharing the same type:

    * Used to instantiate container-like attributes in an Entity
    * Type checks all elements of the container
    * Has append() method to add new elements to container
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

    * Attributes can be defined on instantiation via kwargs
    * Container attributes have special functionality:
        * Instantiates with a list
        * Generates a special method that appends to this list
        * This class is expected to act as a MixIn for Domain Objects
    """
    def __init__(self, allowable_attributes=None, allowable_collections=None, **kwargs):
        self.created_at = time.time()
        defined_attributes = set(kwargs.keys())
        self.expected_attributes = set(allowable_attributes) if allowable_attributes else set()
        self.expected_collections = set(allowable_collections.keys()) if allowable_collections else set()

        for kw in self.expected_attributes.union(defined_attributes).difference(self.expected_collections):
            if kw not in self.expected_attributes.difference(defined_attributes):
                setattr(self, kw, kwargs[kw])
            else:
                setattr(self, kw, None)

        for kw in self.expected_collections:
            if kw in defined_attributes:
                self._add_collection(kw, kwargs[kw])
            else:
                self._add_collection(kw)
            self._instantiate_collection_functions(kw, allowable_collections)

    def empty(self, attributes_to_keep=None, collections_to_keep=None):
        """Filters data from instantiated object (Not recommended for ad hoc use)"""
        assert isinstance(attributes_to_keep, list) | \
            isinstance(collections_to_keep, list), 'Must specify some data to retain in object!'

        if attributes_to_keep:
            for attribute in self.expected_attributes:
                if attribute not in attributes_to_keep:
                    setattr(self, attribute, None)

        if collections_to_keep:
            for attribute in self.expected_collections:
                if attribute not in collections_to_keep:
                    self._add_collection(attribute)

    def _update_created_at(self, timestamp):
        """Update the entity timestamp (Not recommended for ad hoc use)"""
        assert isinstance(timestamp, float) and timestamp <= time.time(), "Timestamp must be Unix timestamp!"
        setattr(self, 'created_at', timestamp)

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
    """A generic Assertion object:

    * The "source" and "target" attributes should both be an Entity
    * The "value" should be some numerical value
    * The "confidence" should be some numerical value
    * The "description" should be a free-form text field
    * The "measure" should be the Entity ascribing semantic meaning to the "value"
    * The "context" should be a list of Tags, Entities, etc that contextualize assertions
    """
    def __init__(self, source, target, value, measure=None, context=None, description=None, confidence=None):
        self.source = source
        self.target = target
        self.value = value
        self.measure = measure
        self.context = context
        self.description = description
        self.confidence = confidence
        self.created_at = time.time()
