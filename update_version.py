import os
import sys
import subprocess


def main():
  project_root = os.path.abspath(os.path.dirname(__file__))

  # Update git repo
  command = 'python src/utils/update.py'
  docker_args = "docker run -it --rm --name butler -v %s:/home/butler butler %s" % (
    project_root, command)
  completed = subprocess.call(docker_args.split())
  if completed:
    print(
      "Couldn't update the git repo. Try re-installing the program instead. This update script doesn't work for ssh-cloned repos, use https"
    )
    sys.exit(1)

  # Build docker image
  command = 'python setup/build_docker.py'
  subprocess.call(command.split())
  print('\nDocker image rebuilt')
  print('Update finished!')


if __name__ == '__main__':
  main()
