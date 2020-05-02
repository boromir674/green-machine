from abc import ABC, abstractmethod, ABCMeta


class DataframeSubject(ABC):
    """
    The DataframeSubject interface declares common operations for both RealSubject and
    the DataframeProxy. As long as the client works with RealSubject using this
    interface, you'll be able to pass it a proxy instead of a real subject.
    """
    @abstractmethod
    def assign(self, **kwargs):
        raise NotImplementedError

    @property
    @abstractmethod
    def columns(self):
        raise NotImplementedError

    @abstractmethod
    def _get_numeric_data(self):
        raise NotImplementedError

    @abstractmethod
    def request(self) -> None:
        pass


# class RealSubject(DataframeSubject):
#     """
#     The RealSubject contains some core business logic. Usually, RealSubjects are
#     capable of doing some useful work which may also be very slow or sensitive -
#     e.g. correcting input data. A DataframeProxy can solve these issues without any
#     changes to the RealSubject's code.
#     """
#
#     def request(self) -> None:
#         print("RealSubject: Handling request.")

from pandas import DataFrame

class DataframeProxy(DataFrame):
    """
    The DataframeProxy has an interface identical to the RealSubject.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self, *args, **kwargs)
        self._columns = {
            'numerical': lambda: [_ for _ in self.columns if _ in self._get_numeric_data().columns.values],
            'categorical': lambda: [_ for _ in self.columns if _ in list(set(self.columns) - set(self._get_numeric_data().columns.values))]}

    def variables(self, var_type):
        return self._columns[var_type]()

    def assign(self, **kwargs):
        return self._real_subject.assign(**kwargs)

    @property
    def columns(self):
        return self._real_subject.columns

    @abstractmethod
    def _get_numeric_data(self):
        return self._real_subject._get_numeric_data()

    def request(self) -> None:
        """
        The most common applications of the DataframeProxy pattern are lazy loading,
        caching, controlling the access, logging, etc. A DataframeProxy can perform one
        of these things and then, depending on the result, pass the execution to
        the same method in a linked RealSubject object.
        """

        if self.check_access():
            self._real_subject.request()
            self.log_access()

    def check_access(self) -> bool:
        print("DataframeProxy: Checking access prior to firing a real request.")
        return True

    def log_access(self) -> None:
        print("DataframeProxy: Logging the time of request.", end="")


class DataHandlerInterface(metaclass=ABCMeta):
    def get_all_variables(self, *args, **kwargs):
        raise NotImplementedError
    def get_categorical_variables(self, *args, **kwargs):
        """call this to get the categorical/discrete variables; either 'nominal' or 'ordinal'"""
        raise NotImplementedError
    def get_numerical_variables(self, *args, **kwargs):
        """call this to get the numerical/continuous variables; either 'interval' or 'ratio'"""
        raise NotImplementedError
    # def get_nominal_variables(self, *args, **kwargs):
    #     """call this to get the nominal variables; discrete variables with undefined ordering"""
    #     raise NotImplementedError
    # def get_ordinal_variables(self, *args, **kwargs):
    #     """call this to get the ordinal variables; discrete variables with a defined ordering"""
    #     raise NotImplementedError
    # def get_interval_variables(self, *args, **kwargs):
    #     """call this to get the interval variables; numerical variables where differences are interpretable; supported operations: [+, -]; no true zero; eg temperature in centigrade (ie Celsius)"""
    #     raise NotImplementedError
    # def get_ratio_variables(self, *args, **kwargs):
    #     """call this to get the ratio variables; numerical variables where all operations are supported (+, -, *, /) and true zero is defined; eg weight"""
    #     raise NotImplementedError


#########################################

class Implementation(DataHandlerInterface, ABC):
    """
    The Implementation defines the interface for all implementation classes. It
    doesn't have to match the Abstraction's interface. In fact, the two
    interfaces can be entirely different. Typically the Implementation interface
    provides only primitive operations, while the Abstraction defines higher-
    level operations based on those primitives.
    """
    pass


class Abstraction:
    """
    The Abstraction defines the interface for the "control" part of the two
    class hierarchies. It maintains a reference to an object of the
    Implementation hierarchy and delegates all of the real work to this object.
    """

    def __init__(self, implementation: Implementation) -> None:
        self.implementation = implementation
    #
    # def operation(self) -> str:
    #     return (f"Abstraction: Base operation with:\n"
    #             f"{self.implementation.operation_implementation()}")


# class ExtendedAbstraction(Abstraction):
#     """
#     You can extend the Abstraction without changing the Implementation classes.
#     """
#
#     def operation(self) -> str:
#         return (f"ExtendedAbstraction: Extended operation with:\n"
#                 f"{self.implementation.operation_implementation()}")
#

"""
Each Concrete Implementation corresponds to a specific platform and implements
the Implementation interface using that platform's API.
"""


class DataManager(Implementation):
    def get_all_variables(self, *args, **kwargs):
        return args[0].columns

    def get_categorical_variables(self, *args, **kwargs):
        return args[0].variables('categorical')

    def get_numerical_variables(self, *args, **kwargs):
        return args[0].variables('numerical')
    #
    # def operation_implementation(self) -> str:
    #     return "DataManager: Here's the result on the platform A."
