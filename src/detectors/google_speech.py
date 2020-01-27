import sys
import ffmpeg
from pathlib import Path

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums, types
from google.api_core.exceptions import ResourceExhausted

from src.utils import ffmpeg_utils
from src.utils import google_utils
from src.utils import meta_utils
from .speech_detector import SpeechRecognizer


class GoogleSpeechRecognition(SpeechRecognizer):
  def __init__(self, commandword_bias):
    super().__init__(commandword_bias)
    self.client = speech.SpeechClient()

  def transcribe_audio(self, audio):
    phrases = [c.command_variant for c in self.commands]
    config = types.RecognitionConfig(
      encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
      language_code='en-US',
      audio_channel_count=2,
      enable_word_time_offsets=True,
      model='video',
      speech_contexts=[dict(phrases=phrases, boost=self.commandword_bias)])

    try:
      operation = self.client.long_running_recognize(config, audio)
    except ResourceExhausted:
      err_msg = f"The project has run out of it's quota for today. Try again tomorrow or set up your own Google Cloud project, see '{meta_utils.install_url()}'"
      print(err_msg)
      sys.exit(1)

    print(u"Analyzing speech...")
    response = operation.result()

    words = []
    for result in response.results:
      for word in result.alternatives[0].words:
        words.append(word)
    return words

  def prepare_data(self, path, google_bucket_name, unique_cloud_id):
    path = str(path).replace('file:', '').replace('%20', ' ')
    path = Path(path)
    assert path.exists(), f"File '{path}' doesn't exist"
    assert path.is_file(), f"Path '{path}' wasn't a file"
    tmp_audio_file = f'/tmp/{unique_cloud_id}_{path.stem}.wav'
    cloud_path = Path(tmp_audio_file)

    ffmpeg.input(path).output(tmp_audio_file).overwrite_output().run(
      quiet=True)

    # Limits video length for price reasons
    n_allowed_minutes = 15
    n_allowed_secs = n_allowed_minutes * 60
    media_duration = ffmpeg_utils.stream_duration(tmp_audio_file)
    err_msg = f"The media files needs to be shorter than {n_allowed_secs} seconds. '{path.name}' was {media_duration} seconds. If you want to analyze longer files, see '{meta_utils.install_url()}'"
    assert media_duration <= n_allowed_secs, err_msg

    if not google_utils.blob_exists(google_bucket_name, cloud_path.name):
      print(f"Uploading file {cloud_path.name} to Google Storage...")

      google_utils.upload_blob(google_bucket_name, tmp_audio_file,
                               cloud_path.name)

    uri_path = f'gs://{google_bucket_name}/' + cloud_path.name
    audio = {"uri": uri_path}
    return audio, cloud_path.name
