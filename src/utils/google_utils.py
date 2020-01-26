from google.cloud import storage
import os
import urllib.request

from . import meta_utils


def upload_blob(bucket_name, source_file_name, destination_blob_name):
  ''' Uploads a file/folder to the bucket '''
  blob = make_blob(bucket_name, destination_blob_name)
  blob.upload_from_filename(source_file_name)


def delete_blob(bucket_name, filename):
  blob = make_blob(bucket_name, filename)
  if blob.exists():
    blob.delete()


def blob_exists(bucket_name, filename):
  return make_blob(bucket_name, filename).exists()


def make_blob(bucket_name, filename):
  client = storage.Client()
  bucket = client.get_bucket(bucket_name)
  return bucket.blob(filename)


def check_connection_to_bucket(bucket_name, install_guide_path):
  try:
    urllib.request.urlopen('http://google.com')
  except:
    raise ConnectionError("Couldn't connect to the internet")

  client = storage.Client()
  bucket = client.get_bucket(bucket_name)

  try:
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
  except:
    url = f'https://console.cloud.google.com/storage/browser/{bucket_name}'
    err_msg = f"Couldn't connect to Google Storage at '{url}'. See the install guide '{install_guide_path}'"
    raise ConnectionError(err_msg)


def register_credentials(bucket_name):
  cred_file = meta_utils.get_project_root() / '.google_key.json'
  install_guide_path = 'https:TODO'
  err_msg = f"File '{cred_file}' didn't exist. It is needed to authenticate yourself towards Google. See the install guide '{install_guide_path}'"
  assert cred_file.exists(), err_msg
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_file)
  check_connection_to_bucket(bucket_name, install_guide_path)