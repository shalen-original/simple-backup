"""Entry point of the backup application"""
import logging

from pathlib import Path
from datetime import datetime
from importlib import import_module
from shutil import rmtree
import stat
import os
import yaml
from app.command_line_args import parse_args

def main():
    """BACKUP - A simple Python backup utility
    This is a simple Python backup utility: it allows to specify a
    configuration file that will be used to perform a backup. For the usage
    script just run the command without any argument.
    """
    # Initial configuration
    args = parse_args()
    configure_logger(args.profile)
    logger = logging.getLogger('')

    separator = "--------------"

    logger.info("BACKUP - A simple Python backup utility")
    logger.info("By Shalen")
    logger.info(separator)
    logger.info("A copy of this output is being saved in the folder: %s",
                Path('./logs').absolute().as_posix())
    logger.info(separator)
    logger.info("Starting a backup with profile '%s'", args.profile)

    # Loading backup profile
    profile_path = Path(args.profile_directory, args.profile + ".yml")
    logger.info("Loading profile from file: %s", profile_path.absolute().as_posix())
    profile = {}

    try:
        profile = yaml.load(profile_path.read_text())
    except FileNotFoundError:
        logger.error("Unable to load profile file. The file does not exists.")
        logger.error("Aborting backup")
        return

    # Creating TMP directory
    tmp_dir = profile['global']['tmp-directory']
    p_tmp_dir = Path(tmp_dir)

    try:
        os.makedirs(p_tmp_dir)
    except FileExistsError:
        # Directory already exists. Checking if empty
        if os.listdir(p_tmp_dir):
            # Directory not empty. Error and abort
            logger.error(f"The tmp directory '{tmp_dir}' already"
                         + " exists and is not empty. Aborting backup")
            return


    # Running inputs
    mappings = {}
    for input_name in profile['inputs']:
        logger.info(f"Running input '{input_name}'")
        inp = import_module(f"app.inputs.{input_name}")
        mappings[input_name] = inp.backup(profile['inputs'][input_name], tmp_dir)
        logger.info(f"Input '{input_name}' done")

    # Writing mappings to file
    with open(Path(tmp_dir, "mappings.yml"), 'w+') as fout:
        print(yaml.dump(mappings), file=fout)

    # Running verifications
    for input_name in profile['inputs']:
        logger.info(f"Running verification for input '{input_name}'")
        inp = import_module(f"app.inputs.{input_name}")
        valid = inp.verify(profile['inputs'][input_name], mappings[input_name], tmp_dir)
        if valid:
            logger.info(f"Input verification for input '{input_name}' done")
        else:
            logger.error(f"Input verification for input '{input_name}' failed. Aborting backup.")
            return

    # Running outputs
    for output_name in profile['outputs']:
        logger.info(f"Running output '{output_name}'")
        out = import_module(f"app.outputs.{output_name}")
        mappings[output_name] = out.backup(profile['outputs'][output_name], tmp_dir, args.profile)
        logger.info(f"Output '{output_name}' done")

    # Deleting tmp folder
    logger.info("Removing tmp directory")
    rmtree(p_tmp_dir, onerror=del_rw)
    logger.info("Backup DONE.")

def del_rw(action, name, exc):
    """ Removes the readonly flag from a file and deletes it. Useful for shutil.rmtree """
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

def configure_logger(profile):
    """Configures the root logger"""
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)

    file_name = datetime.now().strftime(f"logs/backup_{profile}_%Y_%m_%d_%H_%M_%S.log")
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

if __name__ == "__main__":
    main()
