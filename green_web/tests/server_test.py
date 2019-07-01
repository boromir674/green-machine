import os
import json
import pytest
# import tempfile

from green_web import get_logger_n_app

log, app = get_logger_n_app(environment='testing')


# self.db_fd, green_app.config['DATABASE'] = tempfile.mkstemp()
app = app.test_client()
strain_id1 = 'sour-og'
strain_id2 = 'sour-lemon-og'
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
# map_id1 = 'somoclu_' + app.config['DATASET_ID'] + '_pca_toroid_hexagonal_7_5'
# map_id2 = 'somoclu_' + app.config['DATASET_ID'] + '_random_planar_rectangular_8_4'
# _ = app.post('/api/strain/map', data=json.dumps(map_specs1))  # , headers={"Content-Type": "application/json"}
# with green_app.app_context():
#     flaskr.init_db()


class TestFlask:

    # def tearDown(self):
    #     pass
        # os.close(db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])

    @pytest.mark.parametrize("strain_id, name, flavors, type", [
        ("big-budda-cheese", "big-budda-cheese", ["Cheese", "Earthy", "Pungent"], 'hybrid'),
        ("lavender-jones", "lavender-jones", ["Lavender", "Flowery", "Earthy"], 'hybrid'),
        ("white-siberian", "white-siberian", ["Earthy", "Spicy/Herbal", "Menthol"], 'hybrid'),
        pytest.param("purple-bud",
                     "purple-bud", ["Pine", "Pepper", "Lavender"], 'sativa',
                     marks=pytest.mark.xfail),
    ])
    def test_strain_id_endpoint(self, strain_id, name, flavors, type):
        response = app.get('/api/strain/' + strain_id)
        data = json.loads(response.get_data(as_text=True))
        assert 'flavors' in data
        assert 'name' in data
        assert 'type' in data
        assert data['flavors'] == flavors
        assert data['name'] == name
        assert data['type'] == type

    # def test_map_creation_endpoint(self):
    #     response = app.post('/api/strain/map', data=json.dumps(map_specs2), headers={"Content-Type": "application/json"})
    #     data = json.loads(response.get_data(as_text=True))
    #     assert 'map_id' in data
    #     assert data['map_id'] == self.map_id2
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
