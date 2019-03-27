
import time
from collections import Counter


class GrammarAssertion(object):
    """Assertion in the Domain Grammar"""
    def __init__(self, source, context, measure, value, confidence, description):
        self.source = source
        self.context = context
        self.measure = measure
        self.value = value
        self.confidence = confidence
        self.description = description
        self.timestamp = time.time()


class GrammarRelation(object):
    """Relation in the Domain Grammar"""
    def __init__(self, source, description):
        self.source = source
        self.description = description
        self.timestamp = time.time()


class GrammarCollection(object):
    """Collection in the Domain Grammar"""
    def __init__(self):
        self.members = []
        self.timestamp = time.time()

    def __repr__(self):
        return 'Name: {n}\nProvenance: {p}'.format(
            n=self.__class__.__name__,
            p=get_all_bases(self.__class__)
        )

    def is_member_of(self, other, description):
        return other.members.append(GrammarRelation(source=self, description=description))

    @property
    def describe(self):
        return Counter([(i.source.__class__.__name__, i.description) for i in self.members])


class GrammarObject(object):
    """Object in the Domain Grammar"""
    def __init__(self, implementation=None):
        self.observations = []
        self.implementation = implementation
        self.timestamp = time.time()

    def __repr__(self):
        return 'Name: {n}\nProvenance: {p}\nImplemented: {i}'.format(
            n=self.__class__.__name__,
            p=get_all_bases(self.__class__),
            i=self.is_implemented
        )

    def __call__(self, *args, **kwargs):
        if self.is_implemented:
            return self.implementation(self, *args, **kwargs)
        else:
            raise ValueError('The bound method must be parameter-free and only reference bound attributes!')

    def asserts(self, other, context, measure, value, confidence, description):
        other.observations.append(GrammarAssertion(
            source=self, context=context, measure=measure, value=value,
            confidence=confidence, description=description
        ))

    def is_member_of(self, other, description):
        other.members.append(GrammarRelation(source=self, description=description))

    @property
    def describe(self):
        return Counter([
            (i.context.__class__.__name__,
             i.measure.__class__.__name__,
             i.description) for i in self.observations])

    @property
    def is_implemented(self):
        return callable(self.implementation)


def get_all_bases(cls, bases=None):
    bases = bases or []
    bases.append(cls)
    for c in cls.__bases__:
        get_all_bases(c, bases)
    return ' -> '.join([i.__name__ for i in bases])


def describe_entity(item, indent=''):
    if isinstance(item, GrammarCollection):
        print('{i}{x}'.format(i=indent, x=item.__class__.__name__))
        for i in item.members:
            describe_entity(i, indent='  {i}'.format(i=indent))
    elif isinstance(item, GrammarRelation):
        print('{i}{x}'.format(i=indent, x=(item.source.__class__.__name__, item.description)))
        if getattr(item.source, 'members', None):
            for i in item.source.members:
                describe_entity(i, indent='  {i}'.format(i=indent))
    else:
        pass


def create_new_object(name, base_class=GrammarObject, attributes=None):
    """Factory for Domain Objects"""
    if isinstance(attributes, dict):
        new_class = type(name, (base_class,), attributes)
    else:
        new_class = type(name, (base_class,), {})
    new_class.__doc__ = '{n} in the Domain Grammar'.format(n=name)
    return new_class


def register_method_to_context(context):
    def registration(f):
        return setattr(context, f.__name__, f)

    return registration
