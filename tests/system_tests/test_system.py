import sys

from pytest_testconfig import config
import math
import requests

from mdast_cli.distribution_systems.google_play import GooglePlayAPI
from mdast_cli.distribution_systems.appstore import AppStore
from mdast_cli.distribution_systems.gpapi.googleplay import encrypt_password
from mdast_cli.distribution_systems.gpapi.config import DeviceBuilder
from mdast_cli.distribution_systems.google_play import google_play_download

from mdast_cli.distribution_systems.appstore_client.store import StoreClient, StoreException
from mdast_cli.distribution_systems.appstore import *

from mdast_cli.helpers.const import *
from mdast_cli.helpers.logging import Log
from mdast_cli.helpers.helpers import get_app_path


# Google Play unit tests
def test_google_play_class_clean_init():
    gp_api = GooglePlayAPI()
    assert gp_api.gsfId is None
    assert gp_api.authSubToken is None
    assert gp_api.device_config_token is None
    assert gp_api.dfeCookie is None
    assert gp_api.deviceCheckinConsistencyToken is None
