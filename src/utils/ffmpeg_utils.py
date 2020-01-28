import ffmpeg
import subprocess
from pathlib import Path

from src.utils import meta_utils


def stream_duration(path):
  ''' Returns the duration in seconds for the first steam in an asset '''
  assert Path(path).exists(), f"Media file '{path}' doesn't exist"
  probe = ffmpeg.probe(path)
  str_time = probe['streams'][0]['duration']
  return float(str_time)


def assert_installed():
  err_msg = f"Couldn't run ffmpeg. Make sure that it's installed correctly, see '{meta_utils.install_url()}'"
  try:
    completed = subprocess.run('ffmpeg -h'.split(), capture_output=True)
  except Exception as e:
    raise RuntimeError(err_msg) from e

  if completed.returncode != 0:
    raise RuntimeError(err_msg)
