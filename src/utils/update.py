import sys
import git
import shutil
from datetime import datetime

import meta_utils


def update_version():
  project_dir = meta_utils.get_project_root()
  repo = git.Repo(project_dir)
  # Saves changed files and updates repo
  print("WOOWOW")
  changed_files = [item.a_path for item in repo.index.diff(None)]
  print(changed_files)
  if changed_files:
    date_time = datetime.now().strftime("%Y%d%m-%H%M%S")
    save_dir = project_dir / 'saved_updatefiles' / f'date-{date_time}'
    save_dir.mkdir(parents=True)
    for f in changed_files:
      src_path = project_dir / f
      assert src_path.exists()
      out_path = save_dir / f
      shutil.copy(src_path, out_path)


if __name__ == '__main__':
  try:
    update_version()
  except git.InvalidGitRepositoryError:
    print("\nProject isn't tracked by git. Can't update\n")
    sys.exit(1)
