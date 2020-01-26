import subprocess
import argparse
import sys
import os


def parse_args():
  p = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

  p.add_argument('--xml_file',
                 type=str,
                 required=True,
                 help='Input xml-file to enrich')
  return p.parse_known_args()


def main():
  args, _ = parse_args()
  project_root = os.path.abspath(os.path.dirname(__file__))

  command = '/bin/bash'
  host = '/host_root'
  raw_args = ' '.join(sys.argv[1:])
  command = 'python enrich_xml.py --path_base=%s %s' % (host, raw_args)

  docker_args = "docker run -it --rm --name stick -v /:%s:ro -v %s:/home/sticker sticker %s" % (
    host, project_root, command)

  exit_code = subprocess.call(docker_args.split())

  # Exit code 42 means that we want to send xml to Final Cut
  if exit_code == 42:
    xml_filename = os.path.basename(args.xml_file)
    xml_outpath = os.path.join('output', xml_filename)
    send_xml_to_finalcut(os.path.abspath(xml_outpath))


def send_xml_to_finalcut(xml_path):
  assert os.path.exists(xml_path), "XML file '{}' didn't exist" % xml_path
  args = ['osascript', 'src/finalcut/send_xml_to_finalcut.scpt', xml_path]
  subprocess.call(args)


if __name__ == '__main__':
  main()
