import sys
import git
import shutil
from datetime import datetime

import meta_utils


def update_version():
  ''' Saves changed files and resets repo to origin/master (i.e. updates) '''
  project_dir = meta_utils.get_project_root()
  repo = git.Repo(project_dir)
  changed_files = [item.a_path for item in repo.index.diff(None)]

  # Save changed files
  if changed_files:
    date_time = datetime.now().strftime("%Y%d%m-%H%M%S")
    save_dir = project_dir / 'saved_updatefiles' / f'date-{date_time}'
    save_dir.mkdir(parents=True)
    print(f"Saving changed files in '{save_dir}'")
    for f in changed_files:
      src_path = project_dir / f
      out_path = save_dir / f
      out_path.parent.mkdir(parents=True, exist_ok=True)
      assert src_path.exists()
      shutil.copy(src_path, out_path)

  # Update repo
  print('\nUpdating program...\n\n')
  for remote in repo.remotes:
    remote.fetch()

  repo.git.reset('--hard', 'origin/master')
  print('\nUpdating finished!\n\n')


if __name__ == '__main__':
  try:
    update_version()
  except git.InvalidGitRepositoryError:
    print("\nProject isn't tracked by git. Can't update\n")
    sys.exit(1)
