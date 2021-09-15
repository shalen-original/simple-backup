""" Output system that takes the content of the temporary directory and zips it"""

import logging
from pathlib import Path
from shutil import make_archive
from datetime import datetime

def backup(zip_cfg, tmp_dir, profile):
    """ Take the content of tmp_dir and creates a zip. That zip is saved in the given location"""
    logger = logging.getLogger('')

    now_s = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_file_name = Path(zip_cfg["directory"], f"backup-{profile}-{now_s}")

    logger.info("Zipping tmp directory. The output archive will be '%s.zip'", out_file_name)
    make_archive(out_file_name, 'zip', tmp_dir)
