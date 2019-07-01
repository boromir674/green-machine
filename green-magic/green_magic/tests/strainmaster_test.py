import os
import shutil
import pytest
from random import randint
from green_magic.strainmaster import StrainMaster
from green_magic.strain_dataset import StrainDataset
from green_magic.clustering import ClusteringFactory, DistroReporter, get_model_quality_reporter

# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).
# unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)


# @pytest.fixture(scope='module')
# def

# CONSTANTS
my_dir = os.path.dirname(os.path.realpath(__file__))
datasets_dir = my_dir + '/' + 'dts'
graphs_dir = my_dir + '/' + 'graphs'
test_file = 'strain-test-set-100.jl'

dt_path = my_dir + '/' + test_file
all_vars = ['type', 'effects', 'medical', 'negatives', 'flavors']
active_vars = ['type', 'effects', 'medical', 'negatives', 'flavors']
dataset_id = 'test'


if not os.path.exists(datasets_dir):
    os.makedirs(datasets_dir)
if not os.path.exists(graphs_dir):
    os.makedirs(graphs_dir)

# global sm, som, clusters
sm = StrainMaster(datasets_dir=datasets_dir, graphs_dir=graphs_dir)
clf = ClusteringFactory(sm)
# r = DistroReporter()

dt = sm.create_strain_dataset(dt_path, dataset_id)
dt.use_variables(active_vars)
sm.dt.clean()

vs = sm.get_feature_vectors(sm.dt)
som = sm.map_manager.get_som('toroid.rectangular.10.10.random')

clusters = clf.create_clusters(som, 'kmeans', nb_clusters=3, vars=all_vars, ngrams=1)
qr = get_model_quality_reporter(sm, dataset_id)
qr.measure(clusters, metric='silhouette')
qr.measure(clusters, metric='cali-hara')


class TestStrainMaster:

    @classmethod
    def tear_down_class(cls):
        shutil.rmtree(datasets_dir)
        shutil.rmtree(graphs_dir)

    def test_dataset_creation(self):
        assert isinstance(dt, StrainDataset)
        assert sorted(list(active_vars)) == sorted(list(dt.active_variables))
        assert not dt.has_missing_values
        assert len(dt.full_df.columns) == len(active_vars)
        # self.assertCountEqual(active_vars, self.wm.dt.active_variables)  # a and b have the same elements in the same number, regardless of their order
        # self.assertFalse(self.wm.dt.has_missing_values)  # bool(x) is False
        # self.assertEqual(len(self.wm.dt.full_df.columns), len(active_vars))

        assert len(sm.dt) == 98
        assert len(sm.dt.datapoints[0]) == 72
        # self.assertEqual(len(self.wm.dt), 98)
        # self.assertEqual(len(self.wm.dt.datapoints[0]), 72)

    def test_save_load(self):
        sm.save_dataset(dataset_id)
        sm.load_dataset(dataset_id + '-clean.pk')

    def test_som_creation(self):
        assert som.bmus.shape[0] == len(sm.dt)

        assert som.codebook.shape == (10, 10, len(sm.dt.datapoints[0]))

        assert som.umatrix.shape == (10, 10)

        # TODO : uncomment self.assertMultiLineEqual(self.som._map_type, 'toroid')

    def test_cluster_functions(self):
        assert len(clusters) == 3
        assert sum([len(_) for _ in clusters]) == len(sm.dt)
