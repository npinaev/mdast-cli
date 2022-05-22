import math
import subprocess
import sys

import requests
from pytest_testconfig import config

from mdast_cli.distribution_systems.appstore import *
from mdast_cli.distribution_systems.appstore import AppStore
from mdast_cli.distribution_systems.appstore_client.store import StoreClient, StoreException
from mdast_cli.distribution_systems.google_play import GooglePlayAPI, google_play_download
from mdast_cli.distribution_systems.gpapi.config import DeviceBuilder
from mdast_cli.distribution_systems.gpapi.googleplay import encrypt_password
from mdast_cli.helpers.const import *
from mdast_cli.helpers.helpers import get_app_path
from mdast_cli.helpers.logging import Log


def test_get_help(capfd):
    get_help = subprocess.run(
        ['python3', f'{os.getcwd()}/mdast_cli/mdast_scan.py', '-h'])
    out, err = capfd.readouterr()
    assert get_help.returncode == 0
    assert "Select how to download file: appstore/google_play" in out
