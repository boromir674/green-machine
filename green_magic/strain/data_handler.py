from abc import ABCMeta

import attr

from green_magic.interfaces import *

from .d_interfaces import DataHandlerInterface
import strain.df_operations as dfop


class DataHandler(DataHandlerInterface, metaclass=ABCMeta):
    subclasses = {}
    @classmethod
    def register_as_subclass(cls, handler_type):
        def wrapper(subclass):
            cls.subclasses[handler_type] = subclass
            return subclass
        return wrapper

    @classmethod
    def create(cls, handler_type, *args, **kwargs):
        if handler_type not in cls.subclasses:
            raise ValueError('Bad "DataHandler" type \'{}\''.format(handler_type))
        return cls.subclasses[handler_type](*args, **kwargs)


@DataHandler.register_as_subclass('df-handler')
class DataFHandler(DataHandlerInterface):

    def get_all_variables(self, *args, **kwargs):
        return args[0].columns

    def get_categorical_variables(self, *args, **kwargs):
        return dfop.categorical_feats(args[0])

    def get_numerical_variables(self, *args, **kwargs):
        return dfop.numerical_feats(args[0])


# @attr.s
# class DataHandler1(Normalization, Discretization, Encoding):
#     features = attr.ib(init=True, default=[])
#
#     def normalize(self, dataset):
#         return dataset
#
#     def discretize(self, *args, **kwargs):
#         return args[0]
#
#     def encode(self, *args, **kwargs):
#         pass
#
#
#
# @attr.s
# class DataframeHandler(DataHandlerInterface):
#     df = attr.ib(init=True)
#
#     @classmethod
#     def from_csv(cls, file_path):
#         return DataframeHandler(pd.read_csv(file_path))
#
#     def normalize(self, dataset):
#         return dataset
#
#     def discretize(self, *args, **kwargs):
#         return args[0]
#
#     def encode(self, *args, **kwargs):
#         pass
#
#     def split_attributes(dataframe):
#         """Return the categorical and numerical columns/attributes of the given dataframe"""
#         _ = dataframe._get_numeric_data().columns.values
#         return list(set(dataframe.columns) - set(_)), _
#
#
# class DataframeBackend:
#     @staticmethod
#     def split_attributes(dataframe):
#         """Return the categorical and numerical columns/attributes of the given dataframe"""
#         _ = dataframe._get_numeric_data().columns.values
#         return list(set(dataframe.columns) - set(_)), _
