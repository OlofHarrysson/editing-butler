import anyfig

from src.detectors.google_speech import GoogleSpeechRecognition
from src.utils import google_utils
from datetime import datetime


@anyfig.config_class
class UserConfig():
  def __init__(self):
    # Every line that starts with a # is a comment and is not used by the program

    # The name of the google storage bucket
    self.google_bucket_name = 'testytesty'
    # self.google_bucket_name = 'splitter-speechtotext'

    # Sends the enriched xml to Final Cut
    self.send_to_finalcut = True


@anyfig.config_class
class DevConfig(UserConfig):
  def __init__(self):
    super().__init__()

    # The input xml file which contain the data to be analyzed
    self.xml_file = ''

    google_utils.register_credentials(self.google_bucket_name)

    # How sensitively to listen for the command words
    self.commandword_bias = 40
    self.recognizer = GoogleSpeechRecognition(self.commandword_bias)

    # Use fake speech recognition data for debug
    self.fake_data = False

    # Delete contents in projectdir/output before starting
    self.clear_outdir = False

    # Timestamp that gets prepended to the uploaded audiofile
    # TODO: Move this to upload function+add uuid. Have fake-data control if we run from already uploaded file
    self.unique_cloud_file_id = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    self.delete_cloud_file = True

    # When script is ran from docker and volume is mounted in this can help to map xml_paths to the mounted volume
    self.path_base = ''


@anyfig.config_class
class DebugConfig(DevConfig):
  def __init__(self):
    super().__init__()
    self.xml_file = 'input_xml/sofa_event.fcpxml'  # TODO: Doesn't work with abs path & docker
    self.send_to_finalcut = True
    self.fake_data = True
    self.clear_outdir = True
    self.unique_cloud_file_id = ''
    self.delete_cloud_file = False
