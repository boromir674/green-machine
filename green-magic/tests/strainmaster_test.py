import os
import shutil
import unittest
from random import randint
from green_magic.strainmaster import StrainMaster
from green_magic.strain_dataset import StrainDataset
from green_magic.clustering import ClusteringFactory, DistroReporter, get_model_quality_reporter

# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).
unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)

# CONSTANTS
my_dir = os.path.dirname(os.path.realpath(__file__))
datasets_dir = my_dir + '/' + 'dts'
graphs_dir = my_dir + '/' + 'graphs'
test_file = 'strain-test-set-100.jl'

dt_path = my_dir + '/' + test_file
all_vars = ['type', 'effects', 'medical', 'negatives', 'flavors']
active_vars = ['type', 'effects', 'medical', 'negatives', 'flavors']
wd = 'test'
sm = None
som = None
cls = None


def setUpModule():
    if not os.path.exists(datasets_dir):
        os.makedirs(datasets_dir)
    if not os.path.exists(graphs_dir):
        os.makedirs(graphs_dir)

    global sm, som, cls
    sm = StrainMaster(datasets_dir=datasets_dir, graphs_dir=graphs_dir)
    clf = ClusteringFactory(sm)
    # r = DistroReporter()

    dt = sm.create_strain_dataset(dt_path, wd)
    dt.use_variables(active_vars)
    sm.dt.clean()

    vs = sm.get_feature_vectors(sm.dt)
    som = sm.map_manager.get_som('toroid.rectangular.10.10.random')

    cls = clf.create_clusters(som, 'kmeans', nb_clusters=3, vars=all_vars, ngrams=1)
    qr = get_model_quality_reporter(sm, wd)
    qr.measure(cls, metric='silhouette')
    qr.measure(cls, metric='cali-hara')


def tearDownModule():
    global sm, som, cls
    del sm
    del som
    del cls
    shutil.rmtree(datasets_dir)
    shutil.rmtree(graphs_dir)


class TestStrainMaster(unittest.TestCase):
    """Unittest."""

    maxDiff, __slots__ = None, ()

    def setUp(self):
        """Method to prepare the test fixture. Run BEFORE the test methods."""
        self.wm = sm
        self.som = som
        self.cls = cls

    def tearDown(self):
        """Method to tear down the test fixture. Run AFTER the test methods."""
        pass

    def addCleanup(self, function, *args, **kwargs):
        """Function called AFTER tearDown() to clean resources used on test."""
        pass

    @classmethod
    def setUpClass(cls):
        """Class method called BEFORE tests in an individual class run. """
        pass  # Probably you may not use this one. See setUp().

    @classmethod
    def tearDownClass(cls):
        """Class method called AFTER tests in an individual class run. """
        pass  # Probably you may not use this one. See tearDown().

    def test_dataset_creation(self):
        self.assertIsInstance(self.wm.dt, StrainDataset)  # isinstance(a, b)
        self.assertCountEqual(active_vars, self.wm.dt.active_variables)  # a and b have the same elements in the same number, regardless of their order
        self.assertFalse(self.wm.dt.has_missing_values)  # bool(x) is False
        self.assertEqual(len(self.wm.dt.full_df.columns), len(active_vars))

        self.assertEqual(len(self.wm.dt), 98)
        self.assertEqual(len(self.wm.dt.datapoints[0]), 72)

    def test_save_load(self):
        self.wm.save_dataset(wd)
        self.wm.load_dataset(wd + '-clean.pk')

    def test_som_creation(self):
        self.assertEqual(self.som.bmus.shape[0], len(self.wm.dt))
        self.assertTupleEqual(self.som.codebook.shape, (10, 10, len(self.wm.dt.datapoints[0])))
        self.assertTupleEqual(self.som.umatrix.shape, (10, 10))
        self.assertMultiLineEqual(self.som._map_type, 'toroid')

    def test_cluster_functions(self):
        self.assertEqual(len(self.cls), 3)
        self.assertEqual(sum([len(_) for _ in self.cls]), len(self.wm.dt))


if __name__.__contains__("__main__"):
    # print(__doc__)
    unittest.main(warnings='ignore')
    # Run just 1 test.
    # unittest.main(defaultTest='TestStrainMaster.test_dataset_creation', warnings='ignore')
