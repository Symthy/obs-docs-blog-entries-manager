import xml.etree.ElementTree as ET


def convert_root_node(xml: str) -> ET.Element:
    return ET.fromstring(xml)


def extract_tag_head(root: ET.Element, root_tag: str = 'feed') -> str:
    tag_head = root.tag[:-len(root_tag)]  # tag example: {http://www.w3.org/2005/Atom}feed
    return tag_head
