from serialize.serializer_base import SerializerBase
import tempfile


class FilePath(str):
    pass


class FilePathSerializer(SerializerBase):
    def __init__(self):
        self._deserialized_temporary_files = []

    def serialize(self, memory_value):
        """
        Because we have in-memory serialization, this will simply read the file to string
        """
        with open(memory_value, 'rb') as f:
            res = f.read()
        return res

    def __del__(self):
        for tmp in self._deserialized_temporary_files:
            tmp.close()

    def deserialize(self, serialized_value):
        """
        After deserialization, the FilePath object should be openable-writable (why not?..), hence we write serialized
        value in some temporary storage that will be deleted on program shutdown
        :param serialized_value: path to temporary storage
        :return: 
        """
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'wb') as f:
            f.write(serialized_value)
        self._deserialized_temporary_files.append(tmp)
        return FilePath(tmp.name)
