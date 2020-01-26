from lxml import etree
from pathlib import Path
import subprocess


def read_xml(path):
  path = path.absolute()
  assert path.exists(), f"XML file '{path}' didn't exist"
  tree = etree.parse(str(path))
  root = tree.getroot()
  return tree, root


def save_xml(element, outfile):
  element.write(outfile)
  clean_up_xml(outfile)


def clean_up_xml(xml_file):
  parser = etree.XMLParser(remove_blank_text=True)
  root = etree.parse(xml_file, parser).getroot()
  tree = etree.ElementTree(root)
  tree.write(xml_file, encoding='utf-8', pretty_print=True)


def create_element(name, attributes=None):
  if attributes == None:
    attributes = {}

  ele = etree.Element(name)
  for k, v in attributes.items():
    ele.set(k, v)

  return ele


def add_children(parent, children):
  [parent.append(c) for c in children]
  return parent


def get_asset_attributes(path):
  tree, root = read_xml(path)
  asset_xmls = root.findall('resources/asset')
  return [a.attrib for a in asset_xmls]


def get_asset_paths(path):
  assets = get_asset_attributes(path)
  paths = [a['src'] for a in assets]
  return [Path(p.replace('file://', '')) for p in paths]
