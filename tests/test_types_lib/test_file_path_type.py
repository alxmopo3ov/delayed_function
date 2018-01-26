from types_lib.file_path import FilePath, FilePathSerializer
import tempfile
import pytest
import os


@pytest.yield_fixture()
def some_file():
    with tempfile.NamedTemporaryFile() as tmp:
        yield tmp.name


@pytest.yield_fixture()
def serializer():
    return FilePathSerializer()


def test_file_path_write(some_file):
    with open(FilePath(some_file), 'wt') as f:
        f.write('123')
    with open(some_file, 'rt') as f:
        assert f.read() == '123'


def test_file_path_read(some_file):
    with open(some_file, 'wt') as f:
        f.write('123')
    with open(FilePath(some_file), 'rt') as f:
        assert f.read() == '123'


def test_file_path_serialize(some_file, serializer):
    with open(some_file, 'wt') as f:
        f.write('Hello, world!')

    res = serializer.serialize(FilePath(some_file))
    assert res == b'Hello, world!'
    deserialized = serializer.deserialize(res)
    with open(deserialized, 'rt') as f:
        assert f.read() == 'Hello, world!'


def test_file_path_serializer_close_files():
    tmp = tempfile.NamedTemporaryFile()

    def _inner_call():
        s = FilePathSerializer()
        s._deserialized_temporary_files.append(tmp)

    assert os.path.exists(tmp.name)
    _inner_call()
    assert not os.path.exists(tmp.name)
