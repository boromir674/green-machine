import os
import green_magic

from green_magic import StrainMaster
from green_web.config import TestingConfig

basedir = os.path.abspath(os.path.dirname(__file__))

data_dir = os.path.join(basedir, '../../data')
# figures_dir = os.path.join(data_dir, 'figures')
strains_jl = os.path.join(data_dir, 'strain_jsons_2194_fixed_mixed_frow_info.jl')

SM = StrainMaster()

# VARS = ['type', 'effects', 'medical', 'negatives', 'flavors']

# if not os.path.isdir(figures_dir):
#     os.makedirs(figures_dir)

# SM.create_strain_dataset(strains_jl, DATASET_ID)

# SM.dt.use_variables(VARS)
# SM.dt.clean()
# vectors = SM.get_feature_vectors(SM.dt)
# _ = SM.get_feature_vectors(SM.dt)

# clusters = SM.cluster_manager.get_clusters(som, nb_clusters=10)
# clusters.print_clusters(threshold=7, prec=3)

# SM.save_dataset(DATASET_ID)


def get_strain_info(strain_id):
    return SM.dt[strain_id]


def get_strain_coordinates(strain_id):

    x = SM.som.bmus[SM.dt.id2index[strain_id]][0]
    y = SM.som.bmus[SM.dt.id2index[strain_id]][1]
    # print(SM.map_manager.map_obj2id)
    # print(SM.som)
    # print(SM.som in SM.map_manager.map_obj2id)
    return {
        'map_specs': mapid2specs(SM.map_manager.map_obj2id[SM.som]),
        'x': x,
        'y': y
    }


def get_strains_names(coordinates):
    return {'strains-list': SM.strain_names(coordinates)}


def create_som(som_specs_model):
    specs_string = '.'.join(map(lambda x: str(x), (som_specs_model['type'], som_specs_model['grid'], som_specs_model['rows'], som_specs_model['columns'], som_specs_model['initialization'])))
    som = SM.map_manager.get_som(specs_string)
    # print(som == SM.som)
    # print(som in SM.map_manager.map_obj2id)
    # print(SM.som in SM.map_manager.map_obj2id)
    return {
        'map_id': SM.map_manager.map_obj2id[som]
    }


def list_maps():
    return {'maps': sorted([map_id for map_id in SM.map_manager.id2map_obj.keys()])}


def mapid2specs(mapid):
    return {'type': mapid.split('_')[3],
            'grid': mapid.split('_')[4],
            'rows': mapid.split('_')[5],
            'columns': mapid.split('_')[6],
            'initialization': mapid.split('_')[2]}


def create_dataset(dataset_specs):
    dataset = SM.create_strain_dataset(strains_jl, dataset_specs['_id'])
    dataset.use_variables(dataset_specs['active_vars'])
    dataset.clean()
    _ = SM.get_feature_vectors(dataset)
    SM.save_dataset(dataset_specs['_id'])
    return {
        'size': len(dataset),
        'active_vars': dataset.active_variables,
        'vec_len': len(dataset.datapoints[0])
    }


def load_dataset(dataset_id):
    SM.load_dataset(dataset_id + '-clean.pk')
    return {
        'size': len(SM.dt),
        'active_vars': SM.dt.active_variables,
        'vec_len': len(SM.dt.datapoints[0])
    }
