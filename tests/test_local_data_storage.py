from container.local_data_storage import LocalDataStorage


def test_interface():
    storage = LocalDataStorage()
    storage.inputs['ahaha'] = 2
    storage.outputs[0] = 'hihihi'
    assert storage.inputs['ahaha'] == 2
    assert storage.outputs[0] == 'hihihi'


def test_clear_storage():
    storage = LocalDataStorage()
    storage.inputs['ahaha'] = 2
    storage.outputs[0] = 'hihihi'
    storage.clear()
    assert not storage.inputs
    assert not storage.outputs
