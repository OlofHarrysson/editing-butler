import sys
import anyfig
from pathlib import Path

import config as _
from src.finalcut import edit_xml
from src.utils import google_utils
from src.utils import xml_utils
from src.utils import meta_utils
from src.utils import ffmpeg_utils


def main():
  ffmpeg_utils.assert_installed()
  joke = meta_utils.get_joke()
  print(f'Here is a programming joke while you wait ;)\n\n{joke}\n')

  config = anyfig.setup_config(default_config='DebugConfig')
  if config.clear_outdir:
    meta_utils.clear_outdir()

  xml_path = Path(config.xml_file)
  if xml_path.is_absolute():
    xml_path = Path(config.path_base) / str(xml_path)[1:]

  recognizer = config.recognizer

  analyzed_metadatum = []
  for asset in get_asset_files(xml_path):
    asset_path = Path(config.path_base) / asset['src']

    # Upload data to cloud
    data, cloud_file_name = recognizer.prepare_data(
      asset_path, config.google_bucket_name, config.unique_cloud_file_id)

    # Speech -> text -> actions
    actions = recognizer.find_actions(data, config.fake_data)

    if config.delete_cloud_file:
      print(f"Deleting file {cloud_file_name} from Google storage...")
      google_utils.delete_blob(config.google_bucket_name, cloud_file_name)
    analyzed_metadatum.append(dict(id=asset['id'], actions=actions))

  edit_xml.main(xml_path, analyzed_metadatum)

  if config.send_to_finalcut and config.path_base == '':
    xml_outpath = Path('output') / xml_path.name
    meta_utils.send_xml_to_finalcut(xml_outpath)
  elif config.send_to_finalcut:
    sys.exit(42)


def get_asset_files(path):
  assert path.suffix == '.fcpxml', 'You need to input a final cut pro xml file. They typically end with .fcpxml'
  tree, root = xml_utils.read_xml(path)
  asset_xmls = root.findall('resources/asset')
  return [a.attrib for a in asset_xmls]


if __name__ == '__main__':
  main()
