"""Entry point of the backup application"""
import logging

from pathlib import Path
from datetime import datetime
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

    profile_path = Path(args.profile_directory, args.profile + ".yml")
    logger.info("Loading profile from file: %s", profile_path.absolute().as_posix())


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
