import logging

from flask import request
from flask_restplus import Resource
from green_web.api.restplus import api
from green_web.api.business import create_dataset, load_dataset, list_datasets, show_selected_dataset
from green_web.api.serializers import dataset_specs, dataset_info, current_dataset

# from green_web.api.serializers import base_strain

log = logging.getLogger(__name__)

ns = api.namespace('data', description='Data operations related to cannabis strains')


@ns.route('/dataset_new')
# @api.doc(params={'dataset_id': 'A new strain_dataset id'})
class DatasetResource(Resource):
    """Stores/deletes strains, creates/loads/deletes datasets"""

    # @ns.route('/new')
    @api.expect(dataset_specs)
    @api.marshal_with(dataset_info)
    def post(self):
        return create_dataset(request.json)


@ns.route('/dataset_load/<string:dataset_id>')
@api.doc(responses={404: 'Dataset not found'}, params={'dataset_id': 'The Strain dataset ID'})
class DatasetLoader(Resource):

    @api.marshal_with(dataset_info)
    def get(self, dataset_id):
        """Load a Strain dataset given id"""
        return load_dataset(dataset_id)

@ns.route('/list-datasets')
class DatasetEnlister(Resource):
    """Lists computed strain datasets"""

    def get(self):
        """Lists StrainDataset instances"""
        return list_datasets()

@ns.route('/selected-dataset')
class SelectedDatasetShow(Resource):
    """Shows the currently selected strain dataset"""

    @api.marshal_with(current_dataset)
    def get(self):
        """Shows the currently selected StrainDataset instance"""
        return show_selected_dataset()

# @ns.route('/strain/<string:strain_id>')
# @api.doc(responses={404: 'Strain not found'}, params={'strain_id': 'The Strain ID'})
# class StrainFetcher(Resource):
#
#     @api.marshal_with(base_strain)
#     def get(self, strain_id):
#         """Fetch a strain given id"""
#         return mongo.db.strains1.find_one_or_404({'_id': strain_id})
