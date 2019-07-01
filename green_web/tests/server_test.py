import sys
import os
import json
import pytest
# import tempfile

from green_web import get_logger_n_app

my_dir = os.path.dirname(os.path.realpath(__file__))


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


class TestFlask:

    @pytest.mark.parametrize("strain_id, name, flavors, strain_type", [
        ("tesla-tower", "tesla-tower", ["Pepper", "Sweet", "Berry"], 'sativa'),
        ("misty-morning", "misty-morning", ["Spicy/Herbal", "Pine"], 'hybrid'),
        ("alpine-blue", "alpine-blue", ["Berry", "Blueberry", "Pine"], 'hybrid'),
        pytest.param("purple-bud",
                     "purple-bud", ["Pine", "Pepper", "Lavender"], 'sativa',
                     marks=pytest.mark.xfail),
    ])
    def test_strain_id_endpoint(self, strain_id, name, flavors, strain_type, webapp):

        client = webapp.test_client()
        response = client.get('/api/strain/' + strain_id)
        data = json.loads(response.get_data(as_text=True))
        assert 'flavors' in data
        assert 'name' in data
        assert 'type' in data
        assert data['flavors'] == flavors
        assert data['name'] == name
        assert data['type'] == strain_type


    @pytest.mark.parametrize("map_specs, map_id", [
        (map_specs1, 'somoclu_test-environment-dataset_pca_toroid_hexagonal_7_5'),
        (map_specs2, 'somoclu_test-environment-dataset_random_planar_rectangular_8_4')
    ])
    def test_map_creation_endpoint(self, map_specs, map_id, webapp):
        client = webapp.test_client()
        response = client.post('/api/strain/map', data=json.dumps(map_specs), headers={"Content-Type": "application/json"})
        data = json.loads(response.get_data(as_text=True))
        assert 'map_id' in data
        assert data['map_id'] == map_id

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
