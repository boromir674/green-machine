import os
import sys
import json
import pickle
import numpy as np
from .features import WeedLexicon
from .map_maker import MapMakerManager
from .strain_dataset import StrainDataset, create_dataset_from_pickle
from .clustering import get_model_quality_reporter

import logging
_log = logging.getLogger(__name__)


class StrainMaster:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance._datasets_dir = kwargs.get('datasets_dir', './')
            cls.__instance._maps_dir = kwargs.get('maps_dir', './')
        cls.__instance._datasets_dir = kwargs.get('datasets_dir', cls.__instance._datasets_dir)
        cls.__instance._maps_dir = kwargs.get('maps_dir', cls.__instance._maps_dir)
        return cls.__instance

    def __call__(self, *args, **kwargs):
        self._datasets_dir = kwargs.get('_datasets_dir', self._datasets_dir)
        self._maps_dir = kwargs.get('graphs_dir', self._maps_dir)
        self.map_manager.maps_dir = self._maps_dir
        return self

    def __init__(self, datasets_dir=None, graphs_dir=None):
        # self._datasets_dir = datasets_dir
        # if datasets_dir is None:
        #     self._datasets_dir = './'
        # if graphs_dir is None:
        #     graphs_dir = './'
        # self._maps_dir = graphs_dir
        self.id2dataset = {}
        self.selected_dt_id = None
        self.map_manager = MapMakerManager(self, self._maps_dir)
        self.lexicon = WeedLexicon()

    def strain_names(self, coordinates):
        g = ((self.dt.datapoint_index2_id[_], self.som.bmus[_]) for _ in range(len(self.dt)))
        return [n for n, c in g if c[0] == coordinates['x'] and c[1] == coordinates['y']]

    @property
    def dt(self):
        """
        Returns the currently selected/active dataset as a reference to a StrainDataset object.\n
        :return: the reference to the dataset
        :rtype: .strain_dataset.StrainDataset
        """
        return self.id2dataset[self.selected_dt_id]

    @property
    def som(self):
        """
        Returns the currently selected/active som instance, as a reference to a som object.\n
        :return: the reference to the self-organizing map
        :rtype: somoclu.Somoclu
        """
        return self.map_manager.som

    @property
    def model_quality(self):
        return get_model_quality_reporter(self, self.selected_dt_id)

    def get_feature_vectors(self, strain_dataset, list_of_variables=None):
        """
        This method must be called
        :param strain_dataset:
        :param list_of_variables:
        :return:
        """
        if not list_of_variables:
            return strain_dataset.load_feature_vectors()
        else:
            strain_dataset.use_variables(list_of_variables)
            return strain_dataset.load_feature_vectors()

    def create_strain_dataset(self, jl_file, dataset_id, ffilter=''):
        data_set = StrainDataset(dataset_id)
        with open(jl_file, 'r') as json_lines_file:
            for line in json_lines_file:
                strain_dict = json.loads(line)
                if ffilter.split(':')[0] in strain_dict:
                    if strain_dict[ffilter.split(':')[0]] == ffilter.split(':')[1]:  # if datapoint meets criteria, add it
                        data_set.add(strain_dict)
                        if 'description' in strain_dict:
                            self.lexicon.munch(strain_dict['description'])
                else:
                    data_set.add(strain_dict)
                    if 'description' in strain_dict:
                        self.lexicon.munch(strain_dict['description'])
        data_set.load_feature_indexes()
        self.id2dataset[dataset_id] = data_set
        self.selected_dt_id = dataset_id
        return data_set

    def load_dataset(self, a_file):
        strain_dataset = create_dataset_from_pickle(self._datasets_dir + '/' + a_file)
        self.id2dataset[strain_dataset.name] = strain_dataset
        self.selected_dt_id = strain_dataset.name
        _log.info("Loaded dataset with id '{}'".format(strain_dataset.name))
        return strain_dataset

    def save_dataset(self, strain_dataset_id):
        dataset = self.id2dataset[strain_dataset_id]
        if dataset.has_missing_values:
            name = '-not-clean'
        else:
            name = '-clean'
        name = self._datasets_dir + '/' + dataset.name + name + '.pk'
        try:
            with open(name, 'wb') as pickled_dataset:
                pickle.dump(dataset, pickled_dataset, protocol=pickle.HIGHEST_PROTOCOL)
            _log.info("Saved dataset with id '{}' as {}".format(strain_dataset_id, name))
        except RuntimeError as e:
            _log.debug(e)
            _log.info("Failed to save dataset wtih id {}".format(strain_dataset_id))
            pass

    def __getitem__(self, wd_id):
        self.selected_dt_id = wd_id
        return self
