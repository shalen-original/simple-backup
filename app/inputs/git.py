""" Input system that copies all GIT repositories present in a folder"""

import logging
import os

from pathlib import Path
from app.errors.BackupError import BackupError
from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError

def backup(git_cfg, tmp_dir):
    """ Does the backup with the configuration contained in yaml_cfg """
    logger = logging.getLogger('')

    mappings = {}
    counter = 0

    for path in git_cfg['paths']:
        counter += 1

        folder = folder_name(counter)
        dest = Path(tmp_dir, folder)

        mappings[path] = folder
        os.makedirs(dest)

        logger.info("Backing up all repositories in folder '%s' (mapped to '%s')",
                    path, dest.resolve().as_posix())

        if Path(path).is_file():
            raise BackupError(f"Path '{path}' is not a directory.")

        subdirectories = [x for x in Path(path).iterdir() if x.is_dir()]

        for git_repo in subdirectories:
            logger.info("Bundling repository '%s'", git_repo.resolve().as_posix())

            try:
                curr_repo = Repo(git_repo.resolve().as_posix())
                git = curr_repo.git
                git.bundle("create",
                           dest.joinpath(git_repo.resolve().stem + ".bundle").as_posix(), "--all")
            except InvalidGitRepositoryError:
                logger.warning("This is not a valid git repository, skipping.")

    return mappings

def folder_name(counter):
    """ Return the name of a folder generated by this plugin given a counter """
    return f"git{counter}"

def verify(git_cfg, mappings, tmp_dir):
    """ Runs git bundle verify to check the bundles created """
    logger = logging.getLogger('')

    for path in mappings:
        source = Path(path)
        copied = Path(tmp_dir, mappings[path])

        subdirectories = [x for x in source.iterdir() if x.is_dir()]

        for git_repo in subdirectories:
            logger.info("Verifying bundle '%s'",
                        copied.joinpath(git_repo.resolve().stem + ".bundle").as_posix())
            try:
                curr_repo = Repo(git_repo.resolve().as_posix())
                git = curr_repo.git
                bundle_path = Path(copied.joinpath(git_repo.resolve().stem + ".bundle"))
                git.bundle("verify", bundle_path.as_posix())
            except InvalidGitRepositoryError:
                # This means that before a warning has been logged
                pass
            except GitCommandError:
                logger.error("It is not a valid bundle")
                return False

            logger.info("It is valid")


    return True
