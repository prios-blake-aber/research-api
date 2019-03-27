
from collections import Counter


class GrammarRelation(object):
    """Relation in the Domain Grammar"""
    def __init__(self, entity, description):
        self.entity = entity
        self.description = description


class GrammarObject(object):
    """Object in the Domain Grammar"""
    def __init__(self, implementation=None):
        self.members = []
        self.implementation = implementation

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

    def is_member_of(self, other, description):
        return other.members.append(GrammarRelation(entity=self, description=description))

    @property
    def is_implemented(self):
        return callable(self.implementation)

    @property
    def has_members(self):
        return Counter([i.description for i in self.members])


def get_all_bases(cls, bases=None):
    bases = bases or []
    bases.append(cls)
    for c in cls.__bases__:
        get_all_bases(c, bases)
    return ' -> '.join([i.__name__ for i in bases])


def create_new_object(name, base_class=GrammarObject, attributes=None):
    """Factory for Domain Objects"""
    if isinstance(attributes, dict):
        new_class = type(name, (base_class,), attributes)
    else:
        new_class = type(name, (base_class,), {})
    new_class.__doc__ = '{n} in the Domain Grammar'.format(n=name)
    return new_class


def assign_predicate_to_context(functor_name, f, context):
    try:
        context_name = 'Method On A {x}'.format(x=context.__name__)
        return GrammarObject(functor_name, context_name, f)
    except:
        raise ValueError('Registered Context must be in [Meeting, Question, Person, Dot]')


def register_method_to_context(context):
    def registration(f):
        method = assign_predicate_to_context(f.__name__, f, context)
        return setattr(context, f.__name__, method.implementation) or method

    return registration
