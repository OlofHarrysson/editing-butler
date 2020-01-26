from pathlib import Path
import subprocess
'''
Builds the docker image from the parent directory to be able to copy contents from the parent directory into the image
'''


def main():
  args = 'docker build -t butler -f setup/Dockerfile .'
  cwd = Path(__file__).parent.parent.absolute()
  subprocess.run(args.split(), cwd=cwd)


if __name__ == '__main__':
  main()
