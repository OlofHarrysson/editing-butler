import subprocess
import os


def main():
  project_root = os.path.abspath(os.path.dirname(__file__))

  # Update git repo
  command = 'python src/utils/update.py'
  docker_args = "docker run -it --rm --name butler -v %s:/home/butler butler %s" % (
    project_root, command)
  subprocess.call(docker_args.split())

  # Build docker image
  command = 'python setup/build_docker.py'
  subprocess.call(command.split())
  print('\nDocker image rebuilt\n\n')
  print('\nUpdate finished!\n\n')


if __name__ == '__main__':
  main()
