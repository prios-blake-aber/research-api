
"""
TBD
"""

import uuid
import time
from dataclasses import dataclass, field
import typing


@dataclass
class Entity:
    """A generic Entity object

    * This class is expected to act as a MixIn for Domain Objects
    """
    uuid: uuid = uuid.uuid4()
    created_at: int = time.time()
    members: typing.List['Entity'] = field(default_factory=list)

    def empty(self, attributes_to_keep: typing.List[str]):
        """Filters data from instantiated object (Not recommended for ad hoc use)"""
        assert len(attributes_to_keep) > 0, 'Must specify some data to retain in object!'

        if attributes_to_keep:
            for attribute in self.__dict__.keys():
                if attribute not in attributes_to_keep:
                    setattr(self, attribute, None)


@dataclass
class Attribute:
    """Attribute"""
    name: str
    description: str
    members: typing.List['Attribute'] = field(default_factory=list)


@dataclass
class System(Entity):
    description: typing.Optional[str] = 'PriOS'


@dataclass
class Assertion:
    """A generic Assertion object:

    * The "source" and "target" attributes should both be an Entity
    * The "value" should be some numerical value
    * The "confidence" should be some numerical value
    * The "description" should be a free-form text field
    * The "attribute" should be an Attribute
    * The "context" should be a list of Tags, Entities, etc that contextualize assertions
    """
    source: typing.Optional[Entity] = None
    target: typing.Optional[Entity] = None

    # TODO: this is a terrible definition for value
    value: typing.Optional[typing.Union[bool, float, int, str]] = None
    confidence: typing.Optional[float] = None
    description: typing.Optional[str] = None
    attribute: typing.Optional[Attribute] = None
    context: typing.Any = None
    created_at: float = time.time()
    uuid_id: uuid = uuid.uuid4()
