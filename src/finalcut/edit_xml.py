from src.utils import xml_utils


def main(xml_path, analyzed_metadatum):
  tree, root = xml_utils.read_xml(xml_path)

  # Add smart collection
  events = root.findall('./library/event')
  smart_collection = create_smart_collection()
  for event in events:
    event.append(smart_collection)

  # Add metadata
  for analyzed_metadata in analyzed_metadatum:
    found_actions = analyzed_metadata['actions']
    for clip in root.iter('asset-clip'):

      if clip.attrib['ref'] == analyzed_metadata['id']:
        if 'clips' in found_actions:
          keywords = get_clips(found_actions['clips'])
          clip = xml_utils.add_children(clip, children=keywords)

        if 'markers' in found_actions:
          markers = get_markers(found_actions['markers'])
          clip = xml_utils.add_children(clip, children=markers)

  return tree


def create_smart_collection():
  attrs = dict(rule='includes', value='butler')
  m1 = xml_utils.create_element('match-text', attrs)

  attrs = dict(rule='includes', value='marker')
  m2 = xml_utils.create_element('match-text', attrs)

  attrs = dict(name='butler markers', match='all')
  smart_collection = xml_utils.create_element('smart-collection', attrs)

  return xml_utils.add_children(smart_collection, children=[m1, m2])


def get_markers(markers):
  xml_markers = []
  for marker in markers:
    time, tag = marker['time'], marker['name']

    attrs = dict(start=f'{time}s', duration='1s', value=f'butler marker {tag}')
    xml_markers.append(xml_utils.create_element('marker', attrs))

  return xml_markers


def get_clips(clips):
  xml_keywords = []
  for clip in clips:
    start, duration = clip['start_time'], clip['duration']

    attrs = dict(start=f'{start}s',
                 duration=f'{duration}s',
                 value=f'butler clips')
    xml_keywords.append(xml_utils.create_element('keyword', attrs))

  return xml_keywords
