import os
import json

from test_data.constants import Constants


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
                json_string = json.loads(
                    json_to_load.decode(Constants().headers["Accept-Charset"])
                )
            except UnicodeDecodeError:
                json_string = json.loads(json_to_load.decode())
        else:
            json_string = json.loads(json_to_load)
        return json_string

    def get_node(self, node_path):
        """
        get_node return the node of the specific path
        :param node_path:
            path could be defined as json path including nested json array
            example 1: order.date (Simple)
            example 2: ResponseData[0].TRANSACTION[0].TRANDATE' (Nested array)
            example 2: "[0].details.sort_code" ( When start with an array)
        :return:
            node
        """

        json_nodes = str(node_path).split(".")
        data = self.json_data
        index = 0
        for node in json_nodes:
            if node.find("[") > -1:
                start = node.find("[")
                temp_node = node[0:start]
                start = node.find("[") + 1
                end = node.find("]")
                node_index = int(node[start:end])
                try:
                    if index == len(json_nodes) - 1:
                        if temp_node != "":
                            return data[temp_node][node_index]
                        else:
                            return data[node_index]
                    else:
                        if temp_node != "":
                            data = data[temp_node][node_index]
                        else:
                            data = data[node_index]

                except KeyError as e:
                    raise KeyError("JSON Node : " + node_path + " not found")
            else:

                try:

                    if index == len(json_nodes) - 1:
                        return data[node]
                    else:
                        data = data[node]

                except KeyError as e:
                    raise KeyError("JSON Node : " + node_path + " not found")
            index = index + 1

        return None

    def get_value_list_by_node_name(self, node_name, json_data=None):
        """
        get_value_list_by_node_name will return list of all the values of the node_name in json.
        It will recursively traverse the whole json and find the node value and put it in a list
        :param node_name:
            name of the node
        :param json_data:
            value of the node
        :return:
            list of values
        """
        lists = []
        if json_data is None:
            data = self.json_data
        else:
            data = json_data

        for item in data:
            if isinstance(data[item], list):
                value = data[item]
                for x in range(0, len(value)):
                    array_value = data[item][x]
                    lists.extend(
                        self.get_value_list_by_node_name(
                            node_name, json_data=array_value
                        )
                    )
            else:
                if item == node_name:
                    lists.append(data[item])

        return lists

    def get_array_list_by_node_name(self, node_name, node_value, json_data=None):
        """
        This will return the whole section of json if a child node value matches
        :param node_name:
            name of the node
        :param node_value:
            value of the node
        :param json_data:
        :return:
            json dict
        """

        self.found = None
        self.target_data = None

        if json_data is None:
            data = self.json_data
        else:
            data = json_data

        for item in data:
            if isinstance(data[item], list):
                value = data[item]
                for x in range(0, len(value)):
                    array_value = data[item][x]
                    self.get_array_list_by_node_name(
                        node_name, node_value, json_data=array_value
                    )
                    if self.found:
                        break
            else:
                if item == node_name:
                    value = data[item]
                    if str(value) == str(node_value):
                        self.target_data = data
                        self.found = True
                        break

        return self.target_data

    def is_node_exist(self, node_path):
        """
        is_node_exist return true if node exists and false if it doesn't
        :param node_path:
            path could be defined as json path including nested json array
            example 1: order.date (Simple)
            example 2: ResponseData[0].TRANSACTION[0].TRANDATE' (Nested array)
            example 3: "[0].details.sort_code" ( When start with an array)
        :return:
            True or False
        """
        node_exist = False
        node = self.get_node(node_path)
        if node is not None:
            node_exist = True

        return node_exist

    def get_node_value(self, node_path):
        """
        get_node_value retruns the value of a given node
        :param node_path:
        path could be defined as json path including nested json array
            example 1: order.date (Simple)
            example 2: ResponseData[0].TRANSACTION[0].TRANDATE' (Nested array)
            example 3: "[0].details.sort_code" ( When start with an array)
        :return:
        """
        value = None
        node = self.get_node(node_path)
        if node is not None:
            value = node

        return value

    def verify_node_value(self, node_path, expected_value=None):
        """
        validate the value of a given node when expected_value is given. If expected_value is not given it check
        if a value is returned

        :param node_path:
        path could be defined as json path including nested json array
            example 1: order.date (Simple)
            example 2: ResponseData[0].TRANSACTION[0].TRANDATE' (Nested array)
            example 3: "[0].details.sort_code" ( When start with an array)

        :param expected_value:
        :return:
        """
        actual_value = self.get_node_value(node_path)
        if expected_value is not None:
            if type(expected_value) is int:
                assert int(actual_value) == int(expected_value), (
                    "JSON Node : %s, expected node value : %s, didn't match with actual value : %s, "
                    % (node_path, expected_value, actual_value)
                )
            elif type(expected_value) is float:
                assert float(actual_value) == float(expected_value), (
                    "JSON Node : %s, expected node value : %s, didn't match with actual value : %s, "
                    % (node_path, expected_value, actual_value)
                )
            elif expected_value == "null":
                assert (
                    actual_value is None
                ), "JSON Node : %s, expected node value is not Null " % (node_path)
            else:
                assert actual_value == expected_value, (
                    "JSON Node : %s, expected node value : %s, didn't match with actual value : %s, "
                    % (node_path, expected_value, actual_value)
                )
        else:
            assert (
                actual_value is not None
            ), "JSON Node : %s, expected node value is Null " % (node_path)
        return self

    def verify_node_exists(self, node_path):
        """
        validate if specified node exists or not
        :param node_path:
            path could be defined as json path including nested json array
            example 1: order.date (Simple)
            example 2: ResponseData[0].TRANSACTION[0].TRANDATE' (Nested array)
            example 3: "[0].details.sort_code" ( When start with an array)
        :return:
        """
        exists = self.is_node_exist(node_path)
        assert exists == True, "JSON Node : %s doesn't exits" % (node_path)
        return self

    def find_values_from_json_using_key(self, key, json_data):
        results = []

        def _decode_dict(a_dict):
            try:
                results.append(a_dict[key])
            except KeyError:
                pass
            return a_dict

        json.loads(json_data, object_hook=_decode_dict)  # Return value ignored.
        return results
