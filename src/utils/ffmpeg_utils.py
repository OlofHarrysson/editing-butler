import ffmpeg
from pathlib import Path


def stream_duration(path):
  ''' Returns the duration in seconds for the first steam in an asset '''
  assert Path(path).exists(), f"Media file '{path}' doesn't exist"
  probe = ffmpeg.probe(path)
  str_time = probe['streams'][0]['duration']
  return float(str_time)