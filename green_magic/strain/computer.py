import attr
from interfaces.interfaces import Normalization, Discretization, Encoding
from interfaces.types import Ratio, Interval, OrdinalVariable, NominalVariable
from interfaces.visitors import FeatureVisitor

@attr.s
class Computer:
    settings = attr.ib(init=True, default=[])
    feature_computers = attr.ib(init=False, default=attr.Factory(lambda self: self.settings, takes_self=True))


class Normalizer(FeatureVisitor, Normalization):
    def normalize(self, *args, **kwargs):
        pass
    def visit_nominal(self, element: NominalVariable) -> None:
        pass

    def visit_ordinal(self, element: OrdinalVariable) -> None:
        pass

    def visit_interval(self, element: Interval) -> None:
        pass

    def visit_ratio(self, element: Ratio) -> None:
        pass


class Discritizer(FeatureVisitor):
    def discretize(self, *args, **kwargs):
        pass
    def visit_nominal(self, element: NominalVariable) -> None:
        pass

    def visit_ordinal(self, element: OrdinalVariable) -> None:
        pass

    def visit_interval(self, element: Interval) -> None:
        pass

    def visit_ratio(self, element: Ratio) -> None:
        pass


class Encoder(FeatureVisitor, Encoding):
    def encode(self, *args, **kwargs):
        pass
    def visit_nominal(self, element: NominalVariable) -> None:
        pass

    def visit_ordinal(self, element: OrdinalVariable) -> None:
        pass

    def visit_interval(self, element: Interval) -> None:
        pass

    def visit_ratio(self, element: Ratio) -> None:
        pass

class Feature:
    id = attr.ib(init=True)


class DiscreteVariable(Feature):

    def encode(self, schema, values):
        return list(map(lambda x: 1 if x in values else 0, schema))


class SetOfReals(Feature):
    zero = attr.ib(init=True, default=0)

    def encode(self, schema, dict_like):
        return list(map(lambda x: dict_like[x] if x in dict_like else self.zero, dict_like))


class OrdinalVariable(Feature):

    def encode(self, schema, value):
        return [schema[value]]

