from flask import request
from flask_restplus import Resource
from green_web.api.restplus import api

from green_web.api.business import get_strains_names
from green_web.api.serializers import bmu_node_coordinates, strains_list


ns = api.namespace('bmus', description='Operations related to the bmus of the map')


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))


@ns.route('/strains-list')
class StrainsList(Resource):
    """Gets list of strains from a node on the som given coordinates"""

    @api.expect(bmu_node_coordinates)
    @api.marshal_with(strains_list)
    def post(self):
        """Gets list of strains from a node on the som given coordinates"""
        return get_strains_names(request.json)
