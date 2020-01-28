import os
import subprocess
'''
Builds the docker image from the parent directory to be able to copy contents from the parent directory into the image
'''


def main():
  args = 'docker build -t butler -f setup/Dockerfile .'
  project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
  subprocess.call(args.split(), cwd=project_root)


if __name__ == '__main__':
  main()
