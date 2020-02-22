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

  xml_file = args.xml_file
  assert os.path.exists(xml_file), "XML file '%s' didn't exist" % xml_file

  # Raw args to send to main program
  raw_args = ' '.join(sys.argv[1:])

  # xml-files are built on native OS file system so give access to this in docker
  host = '/host_root'

  # The command to run docker with
  command = 'python enrich_xml.py --using_docker=True %s' % raw_args

  project_root = os.path.abspath(os.path.dirname(__file__))
  workdir = '/home/butler/editing-butler'
  docker_args = "docker run -it --rm --name butler -w %s -v /:%s:ro -v %s:%s butler %s" % (
    workdir, host, project_root, workdir, command)

  exit_code = subprocess.call(docker_args.split())

  # Exit code 42 means that we want to send xml to Final Cut
  if exit_code == 42:
    xml_filename = 'enriched_' + os.path.basename(xml_file)
    xml_outpath = os.path.join('output', xml_filename)
    send_xml_to_finalcut(os.path.abspath(xml_outpath))


def send_xml_to_finalcut(xml_path):
  assert os.path.exists(xml_path), "XML file '%s' didn't exist" % xml_path
  args = ['osascript', 'src/finalcut/send_xml_to_finalcut.scpt', xml_path]
  FNULL = open(os.devnull, 'w')
  subprocess.call(args, stdout=FNULL, stderr=subprocess.STDOUT)


if __name__ == '__main__':
  main()
