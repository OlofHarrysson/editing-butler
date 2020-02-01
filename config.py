import anyfig

from src.detectors.google_speech import GoogleSpeechRecognition
from src.utils import google_utils
from datetime import datetime


@anyfig.config_class
class UserConfig():
  def __init__(self):
    # Every line that starts with a # is a comment
    # and is not used by the program
    # You can change configuration of the program here.
    # E.g replace True -> False or 40 -> 60

    # Sends the enriched xml to Final Cut automatically
    self.send_to_finalcut = True

    # Deletes the sound file from google storage after its use
    self.delete_cloud_file = True

    # The input xml file which contain the data to be analyzed
    self.xml_file = ''


@anyfig.config_class
class DevConfig(UserConfig):
  def __init__(self):
    super().__init__()

    # The name of the google storage bucket
    self.google_bucket_name = 'butler-bucket'

    # The credentials file to google cloud
    self.google_key = '.google_key.json'
    google_utils.register_credentials(self.google_bucket_name, self.google_key)

    # How sensitively to listen for the command words
    self.commandword_bias = 40

    # Performs the speech analysis
    self.recognizer = GoogleSpeechRecognition(self.commandword_bias)

    # Use fake speech recognition data for debug
    self.fake_data = False

    # Delete contents in projectdir/output before starting
    self.clear_outdir = False

    # Timestamp that gets prepended to the uploaded audiofile
    # TODO: Move this to upload function+add uuid. Have fake-data control if we run from already uploaded file
    self.unique_cloud_file_id = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    # When script is ran from docker and volume is mounted in this can help to map xml_paths to the mounted volume
    self.path_base = ''


@anyfig.config_class
class DebugConfig(DevConfig):
  def __init__(self):
    super().__init__()
    self.xml_file = 'input_xml/sofa_event.fcpxml'
    self.send_to_finalcut = True
    self.fake_data = True
    self.clear_outdir = True
    self.unique_cloud_file_id = ''
    self.delete_cloud_file = False
