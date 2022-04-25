import os
import json

from test_data.constants import headers


class JSONUtil:
    def __init__(self, json_str=None):
        """JSONUtil can be used to validate any node value, total node count,
            node count of a child, node type and json schema from a file
        :param json_str: A JSON-like object.
        """
        if json_str is not None:
            if isinstance(json_str, dict):
                self.json_data = json_str
            else:
                self.json_data = JSONUtil.load_json(json_str)

    @staticmethod
    def dump_json(obj, indent=None, sort_keys=True):
        """Turn python object into a JSON str

        :param obj: Python obj to turn into a JSON str.
        :param indent: Spaces of indentation per break in JSON. Defaults to None (no indentation).
        :param sort_keys: Whether or not to sort keys in obj. Defaults to True.
        """
        return json.dumps(obj, indent=indent, sort_keys=sort_keys)

    @staticmethod
    def dump_json_to_file(path, obj):
        """Dump JSON-like object to a file

        :param path: Full path to the file on disk. File does not have to currently exist.
        :param obj: JSONifiable python object.
        """

        with open(path, "w") as f:
            f.write(json.dumps(obj, indent=4))

    @staticmethod
    def load_json_from_file(path):
        """Load JSON string from a file into a python dictionary

        :param path: Full path to the file on disk
        :return: JSON object as a str
        """
        if not os.path.exists(path):
            raise FileNotFoundError(
                "Did not find file on disk at '%s' to load from" % path
            )
        with open(path, "r") as f:
            return json.loads(f.read())

    @staticmethod
    def load_json(json_to_load):
        """Turn json str/bytes into a python object
        :param json_to_load: JSON str/bytes/dict to be loaded into a python object.
        """
        if isinstance(json_to_load, bytes):
            try:
                json_string = json.loads(json_to_load.decode(headers["Accept-Charset"]))
            except UnicodeDecodeError:
                json_string = json.loads(json_to_load.decode())
        else:
            json_string = json.loads(json_to_load)
        return json_string
