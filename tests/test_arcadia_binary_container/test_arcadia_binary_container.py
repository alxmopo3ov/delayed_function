from arcadia_binary_container import generate_arcadia_binary_dir
import arcadia_binary_container.generate_arcadia_binary
import pytest
import tempfile
import shutil
import os
import getpass

executable_reference = """import {tempdir}
from some_test_root.environment import Environment
from some_test_root.executable_container.nirvana_container import NirvanaContainer

if __name__ == "__main__":
    env = Environment()
    container_type = env.container_type
    function_name = env.function_name
    container = NirvanaContainer({tempdir}.testing_function)
    container.run()
"""

ya_make_reference = """PROGRAM(nirvana_auto_ml_container)

OWNER({owner})

PY_SRCS(
    __main__.py
)

PEERDIR(
    some_test_root
    {tempdir}
)

END()
"""


@pytest.yield_fixture()
def patch_automl_root(monkeypatch):
    def get_root():
        return 'some_test_root'

    monkeypatch.setattr(arcadia_binary_container.generate_arcadia_binary, 'get_auto_ml_root', get_root)
    yield


@pytest.yield_fixture()
def my_function():
    temp_dir = tempfile.mkdtemp()

    def testing_function(x, y):
        print(x, y)

    testing_function.container_params = {'library_root': temp_dir}
    testing_function.__name__ = 'testing_function'

    yield testing_function, temp_dir
    shutil.rmtree(temp_dir)


def test_generate_arcadia_binary_dir(my_function, patch_automl_root):
    func, folder = my_function
    folder = folder[1:]  # we work with 'relative' import
    res_dir = generate_arcadia_binary_dir(func, True)
    assert res_dir == os.path.join(folder, 'auto_ml_executable_dir')
    with open(os.path.join(res_dir, '__main__.py')) as f:
        res = f.read()
    assert res == executable_reference.format(tempdir=folder.replace('/', '.'))
    with open(os.path.join(res_dir, 'ya.make')) as f:
        res = f.read()
    assert res == ya_make_reference.format(owner=getpass.getuser(), tempdir=folder)
