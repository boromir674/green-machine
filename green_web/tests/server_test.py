import sys
import os
import json
import pytest
# import tempfile

from green_web import get_logger_n_app

# log, app = get_logger_n_app(environment='testing')
my_dir = os.path.dirname(os.path.realpath(__file__))


# self.db_fd, green_app.config['DATABASE'] = tempfile.mkstemp()
# test_app = app.test_client()


# @pytest.fixture(scope='module')
# def client():
#     test_app = app.test_client()
#     _ = test_app.get('/api/data/dataset_load/' + app_config['DATASET_ID'])
#     return test_app

@pytest.fixture(scope='module')
def webapp():
    log, app = get_logger_n_app(environment='testing')
    # app_config = app.config['DATASETS_DIR'] = os.path.join(my_dir, '../../data')
    return app

map_specs1 = {
    'columns': 5,
    'grid': 'hexagonal',
    'initialization': 'pca',
    'rows': 7,
    'type': 'toroid'
}
map_specs2 = {
    'columns': 4,
    'grid': 'rectangular',
    'initialization': 'random',
    'rows': 8,
    'type': 'planar'
}

# with green_app.app_context():
#     flaskr.init_db()


class TestFlask:

    # def tearDown(self):
    #     pass
        # os.close(db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])

    def test_default_dataset(self, webapp):
        print("WN: '{}'".format(getattr(webapp.dt, 'name', '')))
        # print("CN: '{}'".format(getattr(client.dt, 'name', '')))
        assert webapp.dt.name == 'test-environment-dataset'

    @pytest.mark.parametrize("strain_id, name, flavors, strain_type", [
        ("tesla-tower", "tesla-tower", ["Pepper", "Sweet", "Berry"], 'sativa'),
        # ("misty-morning", "misty-morning", ["Spicy/Herbal", "Pine"], 'hybrid'),
        # ("alpine-blue", "alpine-blue", ["Berry", "Blueberry", "Pine"], 'hybrid'),
        pytest.param("purple-bud",
                     "purple-bud", ["Pine", "Pepper", "Lavender"], 'sativa',
                     marks=pytest.mark.xfail),
    ])
    def test_strain_id_endpoint(self, strain_id, name, flavors, strain_type, webapp):
        assert webapp.dt.name == 'test-environment-dataset'
        print("WN: '{}'".format(getattr(webapp.dt, 'name', '')))
        # webapp.config['DATASETS_DIR'] = ''
        client = webapp.test_client()
        _ = client.get('/api/data/dataset_load/' + 'test-environment-dataset')
        response = client.get('/api/data/selected-dataset')
        data = json.loads(response.get_data(as_text=True))
        assert data['id'] == 'test-environment-dataset'
        response = client.get('/api/strain/' + strain_id)
        data = json.loads(response.get_data(as_text=True))
        assert 'flavors' in data
        assert 'name' in data
        assert 'type' in data
        assert data['flavors'] == flavors
        assert data['name'] == name
        assert data['type'] == strain_type

    # @pytest.mark.parametrize("map_specs, map_id", [
    #     (map_specs1, 'somoclu_' + app_config['DATASET_ID'] + '_pca_toroid_hexagonal_7_5'),
    #     (map_specs2, 'somoclu_' + app_config['DATASET_ID'] + '_random_planar_rectangular_8_4')
    # ])
    # def test_map_creation_endpoint(self, map_specs, map_id, web_app):
    #     # with web_app as c:
    #     response = web_app.post('/api/strain/map', data=json.dumps(map_specs), headers={"Content-Type": "application/json"})


        # map_id1 = 'somoclu_' + app.config['DATASET_ID'] + '_pca_toroid_hexagonal_7_5'
        # data = json.loads(response.get_data(as_text=True))
        # assert 'map_id' in data
        # assert data['map_id'] == map_id
        # rv = c.post('/jsonapi', json={
        #     'attr': 'value', 'other': 'data'
        # })
        # json_data = rv.get_json()

        # map_id2 = 'somoclu_' + app.config['DATASET_ID'] + '_random_planar_rectangular_8_4'
        # response = app.post('/api/strain/map', data=json.dumps(map_specs2), headers={"Content-Type": "application/json"})
        # data = json.loads(response.get_data(as_text=True))
        # assert 'map_id' in data
        # assert data['map_id'] == map_id2

    #
    # def test_strain_coordinates_request(self):
    #     response = app.post('/api/strain/' + strain_id2)
    #     data = json.loads(response.get_data(as_text=True))
    #     assert float(data['x']) == int(data['x'])
    #     assert float(data['y']) == int(data['y'])
    #     assert int(data['x']) >= 0
    #     assert int(data['y']) >= 0
    #
    #     assert int(data['x']) <= int(data['map_specs']['columns'])
    #     assert int(data['y']) <= int(data['map_specs']['rows'])

    # dictToSend = self.map_specs
    # res = requests.post('http://localhost:5555/api/strain/map', json=self.map_specs)
    # print('response from server:', res.text)
    # dictFromServer = res.json()
