import subprocess
import os


def main():
  command = 'python src/utils/update.py'
  hej = ''
  project_root = os.path.abspath(os.path.dirname(__file__))
  docker_args = "docker run -it --rm --name butler -v %s:/home/butler butler %s" % (
    project_root, command)

  subprocess.call(docker_args.split())


if __name__ == '__main__':
  main()
