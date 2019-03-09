import timeit


def import_modules():
    from green_magic import WeedMaster
    from green_magic.clustering import ClusteringFactory, DistroReporter, get_model_quality_reporter


def import_time():
    SETUP_CODE = '''
from __main__ import import_modules
    '''

    TEST_CODE = '''
import_modules()
    '''
    sum_times = timeit.timeit(setup=SETUP_CODE,
                        stmt=TEST_CODE,
                        number=100)

    return sum_times


def create_dataset():
    wm = WeedMaster(datasets_dir=datasets_dir, graphs_dir=graphs_dir)
    dt = wm.create_weedataset(dt_path, wd)


def create_dataset_time():
    SETUP_CODE = '''
import os
import shutil
from green_magic import WeedMaster
from green_magic.clustering import ClusteringFactory, DistroReporter, get_model_quality_reporter
from __main__ import create_dataset

my_dir = '/data/projects/knowfly/green-machine/green-magic/green_magic/tests/'

datasets_dir = my_dir + '/' + 'dts'
graphs_dir = my_dir + '/' + 'graphs'
test_file = 'strain-test-set-100.jl'

dt_path = my_dir + '/' + test_file
all_vars = ['type', 'effects', 'medical', 'negatives', 'flavors']
active_vars = ['type', 'effects', 'medical', 'negatives', 'flavors']
wd = 'test'
strain_master = None
som = None
cls = None
if not os.path.exists(datasets_dir):
    os.makedirs(datasets_dir)
if not os.path.exists(graphs_dir):
    os.makedirs(graphs_dir)
strain_master = WeedMaster(datasets_dir=datasets_dir, graphs_dir=graphs_dir)
    '''

    TEST_CODE = '''
dt = strain_master.create_weedataset(dt_path, wd)
        '''
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=3,
                          number=10)
    return times


if __name__ == "__main__":
    # sum_import_times = import_time()
    # print('Importing "sum of times":', sum_import_times)
    list_sum_create_dataset_times = create_dataset_time()
    print('Dataset creation sumation of times across different "runs":', list_sum_create_dataset_times)
