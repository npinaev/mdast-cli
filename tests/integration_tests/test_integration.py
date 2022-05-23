import math
import subprocess
import sys
import random
import string

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


def test_device_builder_mock_device_setup_with_mocked_data():
    fake_device_data = GooglePlayAPI(device_codename='mocked').deviceBuilder.device
    assert fake_device_data['userreadablename'] == 'Mocked Name 123'
    assert fake_device_data['build.hardware'] == 'Mocked'
    assert fake_device_data['build.radio'] == 'Mocked'
    assert fake_device_data['build.bootloader'] == 'Mocked'
    assert fake_device_data['build.fingerprint'] == 'Mocked'
    assert fake_device_data['build.brand'] == 'Mocked'
    assert len(fake_device_data) == 36


def test_device_builder_get_mocked_android_build():
    android_build = GooglePlayAPI(device_codename='mocked').deviceBuilder.getAndroidBuild()
    assert android_build.id == 'Mocked'
    assert android_build.model == 'Mocked'
    assert android_build.sdkVersion == 1337
    assert android_build.buildProduct == 'Mocked'
    assert android_build.googleServices == 1337


def test_google_play_login_needs_browser_check_for_error_no_token():
    gp_api = GooglePlayAPI()
    try:
        gp_api.login(email=config['gp']['test_email'], password=config['gp']['test_pass'], gsfId=None,
                     authSubToken=None)
    except UnboundLocalError as e:
        assert True
        assert e.args[0] == "local variable 'ac2dmToken' referenced before assignment"


def test_google_play_login_fail_fuzzing():
    gp_api = GooglePlayAPI()
    email_fuzzing=''.join(random.choices(string.ascii_lowercase, k=10))
    password_fuzzing=''.join(random.choices(string.ascii_lowercase, k=10))
    try:
        gp_api.login(email=email_fuzzing, password=password_fuzzing, gsfId=None,
                     authSubToken=None)
    except UnboundLocalError as e:
        assert True
        assert e.args[0] == "local variable 'ac2dmToken' referenced before assignment"


def test_google_play_authenticate_and_check_api_works():
    gsfId = config['gp']['gsfid']
    auth_token = config['gp']['authSubToken']
    test_package_name = config['gp']['insta_package_name']
    gp_api = GooglePlayAPI()
    gp_api.login(email=None, password=None, gsfId=int(gsfId), authSubToken=auth_token)
    details = gp_api.details(test_package_name)
    assert len(details) == 21
    assert details['docid'] == test_package_name
    assert details['detailsUrl'] == 'details?doc=com.instagram.android'


def test_google_play_authenticate_fuzzing_check_failed():
    gsfId = 1337
    auth_token = ''.join(random.choices(string.ascii_lowercase, k=10))
    test_package_name = config['gp']['insta_package_name']
    gp_api = GooglePlayAPI()
    gp_api.login(email=None, password=None, gsfId=int(gsfId), authSubToken=auth_token)
    try:
        gp_api.details(test_package_name)
    except ConnectionError as e:
        assert True
        assert "Error retrieving information from server" in e.args[0]


def test_app_store_login_first_try_wrong_pass(capfd):
    apple_id = config['as']['apple_id']
    test_pass = config['as']['test_pass']
    login_no_2fa = subprocess.run(
        ['python3', f'{os.getcwd()}/mdast_cli/mdast_scan.py', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{test_pass}', '--appstore_app_id',
         'aaaa'])
    out, err = capfd.readouterr()
    assert login_no_2fa.returncode == 4
    assert "INFO Logging into iTunes" in out
    assert "ERROR Store authenticate failed! Message: MZFinance.BadLogin.Configurator_message" in out


def test_app_store_login_fuzzing(capfd):
    apple_id = ''.join(random.choices(string.ascii_lowercase, k=10))
    test_pass = ''.join(random.choices(string.ascii_lowercase, k=10))
    login_no_2fa = subprocess.run(
        ['python3', f'{os.getcwd()}/mdast_cli/mdast_scan.py', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{test_pass}', '--appstore_app_id',
         'aaaa'])
    out, err = capfd.readouterr()
    assert login_no_2fa.returncode == 4
    assert "ERROR Store authenticate failed! Message: MZFinance.BadLogin.Configurator_message" in out


def test_app_store_login_and_check_api_works(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    bundle = config['as']['bundle_id']
    login_correct_and_check_api_works = subprocess.run(
        ['python3', f'{os.getcwd()}/mdast_cli/mdast_scan.py', '--distribution_system', 'appstore',
         '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_bundle_id',
         f'{bundle}', '--lookup'])
    out, err = capfd.readouterr()
    assert login_correct_and_check_api_works.returncode == 0
    assert "INFO Successfully logged in as" in out
    assert "Successfully found application" in out

