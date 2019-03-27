
from src import meta

Justification = meta.FunctorFactory(name='Justification', base_class=meta.GrammarObject)
Axiom = meta.FunctorFactory(name='Axiom', base_class=Justification)
Hypothesis = meta.FunctorFactory(name='Hypothesis', base_class=Justification)
