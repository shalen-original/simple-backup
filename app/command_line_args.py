"""Handles the commandline parameters"""

import argparse

def parse_args():
    """Parses the commandline parameters with Argparse
    Returns the output of Argparses.parse_args
    """
    parser = argparse.ArgumentParser(description="BACKUP - A simple Python backup utility")

    # Utility parameters
    parser.add_argument('-v', '--version', action='version', version='0.0.1')

    # Mandatory parameters
    parser.add_argument("profile", help="""The name of the backup profile to be used.
                        It is the name of the YAML file containing the configuration
                        that has to be used for this backup (without extension).""")

    # Optional parameters
    parser.add_argument("-d", "--profile-directory",
                        help="""The directory that contains the profiles usable by the application.
                        Defaults to .\\profiles""", default=".\\profiles")

    return parser.parse_args()
