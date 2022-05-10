from lxml import etree as et
from xml.dom import minidom
import xmltodict

from test_data.constants import Constants


class XMLUtil:
    def __init__(self, xml=None):
        """JSONUtil can be used to validate any node value, total node count,
            node count of a child, node type and json schema from a file
        :param json_str: A JSON-like object.
        """
        if xml is not None:
            self.tree = et.fromstring(xml)
            self.root = et.Element("root")
            self.xml_string = xml

    def load_xml_from_file(self, file_path):
        parsar = et.XMLParser(
            resolve_entities=False, remove_blank_text=True, strip_cdata=False
        )
        self.tree = et.parse(file_path, parsar)
        self.root = et.Element("root")

    def load_from_json(self, json_str):
        xml_str = xmltodict.unparse(json_str)
        self.__init__(str(xml_str).encode(Constants().headers["Accept-Charset"]))

    def get_xml_string(self):
        xml = et.tostring(self.tree)
        reparsed = minidom.parseString(xml)
        xml_string = str(reparsed.toprettyxml(indent="\t"))
        return xml_string

    def print_pretty(self):
        print(self.get_xml_string())

    def convert_to_json_string(self):
        json_string = xmltodict.parse(self.get_xml_string(), process_namespaces=True)
        return json_string

    def modify_node_value(self, node, value):
        elements = self.tree.findall(node)
        for elem in elements:
            elem.text = value
        self.tree.write("output.xml")
        self.print_pretty()
