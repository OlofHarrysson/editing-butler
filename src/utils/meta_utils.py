import pyjokes
import subprocess
from pathlib import Path


def get_project_root():
  return Path(__file__).parent.parent.parent.absolute()


def send_xml_to_finalcut(xml_path):
  xml_path = xml_path.absolute()
  assert xml_path.exists(), f"XML file '{xml_path}' doesn't exist"
  args = ['osascript', 'src/finalcut/send_xml_to_finalcut.scpt', xml_path]
  subprocess.run(args, capture_output=True)


def clear_outdir():
  outdir = get_project_root() / 'output'
  outdir.mkdir(exist_ok=True)
  for p in outdir.iterdir():
    p = p.absolute()
    p.unlink()


def get_joke():
  return pyjokes.get_joke()


def install_url():
  return 'https://www.editingbutler.com/en/markdown/installation'
