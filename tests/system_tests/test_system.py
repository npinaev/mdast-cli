import math
import subprocess
import sys
import time

import requests
from pytest_testconfig import config

from mdast_cli.helpers.const import TAG, PACKAGE_NAMES


# System tests
def test_install_pypi_package(capfd):
    install_pypi = subprocess.run(
        ['pip', 'install', 'poly_app_downloader', '-U'])
    out, err = capfd.readouterr()
    assert install_pypi.returncode == 0
    assert ("Requirement already satisfied" in out or "Successfully installed" in out)


def test_download_docker_image(capfd):
    download_docker_image = subprocess.run(
        ['docker', 'pull', 'npinaev/poly_app_downloader'])
    out, err = capfd.readouterr()
    assert download_docker_image.returncode == 0
    assert "Pulling from npinaev/poly_app_downloader" in out
    assert "Image is up to date for npinaev/poly_app_downloader" in out \
           or "Downloaded newer image for npinaev/poly_app_downloader" in out


def test_pypi_download_from_google_play(capfd):
    gsfid = int(config['gp']['gsfid'])
    authSubToken = config['gp']['authSubToken']
    package_name = config['gp']['insta_package_name']
    download_from_gp = subprocess.run(
        ['poly_app_downloader', '--distribution_system', 'google_play', '--google_play_package_name',
         f'{package_name}', '--google_play_gsfid', f'{gsfid}', '--google_play_auth_token',
         f'{authSubToken}'])
    out, err = capfd.readouterr()
    assert download_from_gp.returncode == 0
    assert "INFO Your application was downloaded!" in out
    assert "INFO Google Play - Logging in with gsfid and auth token" in out
    assert "INFO Google Play - Successfully logged in Play Store" in out
    assert "com.instagram.android" in out


def test_docker_download_from_google_play(capfd):
    gsfid = int(config['gp']['gsfid'])
    authSubToken = config['gp']['authSubToken']
    package_name = config['gp']['insta_package_name']
    download_from_gp = subprocess.run(
        ['docker', 'run', 'npinaev/poly_app_downloader', '--distribution_system', 'google_play',
         '--google_play_package_name', f'{package_name}', '--google_play_gsfid', f'{gsfid}', '--google_play_auth_token',
         f'{authSubToken}'])
    out, err = capfd.readouterr()
    assert "INFO Your application was downloaded!" in out
    assert "INFO Google Play - Logging in with gsfid and auth token" in out
    assert "INFO Google Play - Successfully logged in Play Store" in out
    assert "com.instagram.android" in out


def test_pypi_download_paid_app_from_google_play(capfd):
    gsfid = int(config['gp']['gsfid'])
    authSubToken = config['gp']['authSubToken']
    package_name = config['gp']['paid_app_bouncer_package_name']
    download_unpaid_from_gp = subprocess.run(
        ['poly_app_downloader', '--distribution_system', 'google_play', '--google_play_package_name',
         f'{package_name}', '--google_play_gsfid', f'{gsfid}', '--google_play_auth_token',
         f'{authSubToken}'])
    out, err = capfd.readouterr()
    assert download_unpaid_from_gp.returncode == 4
    assert "Error retrieving information from server. DF-DFERH-01" in out


def test_docker_download_paid_app_from_google_play(capfd):
    gsfid = int(config['gp']['gsfid'])
    authSubToken = config['gp']['authSubToken']
    package_name = config['gp']['paid_app_bouncer_package_name']
    download_unpaid_from_gp = subprocess.run(
        ['docker', 'run', 'npinaev/poly_app_downloader', '--distribution_system', 'google_play',
         '--google_play_package_name', f'{package_name}', '--google_play_gsfid', f'{gsfid}', '--google_play_auth_token',
         f'{authSubToken}'])
    out, err = capfd.readouterr()
    assert download_unpaid_from_gp.returncode == 4
    assert "Error retrieving information from server. DF-DFERH-01" in out


def test_pypi_download_banned_app_from_google_play(capfd):
    gsfid = int(config['gp']['gsfid'])
    authSubToken = config['gp']['authSubToken']
    package_name = config['gp']['banned_app_sber_package_name']
    download_banned_from_gp = subprocess.run(
        ['poly_app_downloader', '--distribution_system', 'google_play', '--google_play_package_name',
         f'{package_name}', '--google_play_gsfid', f'{gsfid}', '--google_play_auth_token',
         f'{authSubToken}'])
    out, err = capfd.readouterr()
    assert download_banned_from_gp.returncode == 4
    assert "Seems like something goes wrong. Item not found" in out


def test_docker_download_banned_app_from_google_play(capfd):
    gsfid = int(config['gp']['gsfid'])
    authSubToken = config['gp']['authSubToken']
    package_name = config['gp']['banned_app_sber_package_name']
    download_banned_from_gp = subprocess.run(
        ['docker', 'run', 'npinaev/poly_app_downloader', '--distribution_system', 'google_play',
         '--google_play_package_name', f'{package_name}', '--google_play_gsfid', f'{gsfid}', '--google_play_auth_token',
         f'{authSubToken}'])
    out, err = capfd.readouterr()
    assert download_banned_from_gp.returncode == 4
    assert "Seems like something goes wrong. Item not found" in out


def test_pypi_lookup_info_about_app_by_bundle_from_app_store(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    bundle_id = config['as']['bundle_id']
    lookup_info = subprocess.run(
        ['poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_bundle_id',
         f'{bundle_id}', '--lookup'])
    out, err = capfd.readouterr()
    assert lookup_info.returncode == 0
    assert "INFO Successfully logged in" in out
    assert "INFO Successfully found application by bundle id (ru.gazprombank.ios.mobilebank) with name:" in out
    assert "app_id: 1406492297" in out


def test_docker_lookup_info_about_app_by_bundle_from_app_store(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    bundle_id = config['as']['bundle_id']
    lookup_info = subprocess.run(
        ['docker', 'run', 'npinaev/poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_bundle_id',
         f'{bundle_id}', '--lookup'])
    out, err = capfd.readouterr()
    assert "INFO Successfully logged in" in out
    assert "INFO Successfully found application by bundle id (ru.gazprombank.ios.mobilebank) with name:" in out
    assert "app_id: 1406492297" in out


def test_pypi_download_app_by_bundle_from_app_store(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    bundle_id = config['as']['bundle_id']
    download_info = subprocess.run(
        ['poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_bundle_id',
         f'{bundle_id}'])
    out, err = capfd.readouterr()
    assert download_info.returncode == 0
    assert "INFO Successfully logged in" in out
    assert "INFO Trying to find app in App Store with bundle id ru.gazprombank.ios.mobilebank" in out
    assert "Successfully found application by bundle id (ru.gazprombank.ios.mobilebank)" in out
    assert "Trying to purchase app with id" in out
    assert "This app was purchased before for" in out
    assert "Downloading app is Газпромбанк" in out
    assert "INFO Your application was downloaded!" in out


def test_docker_download_app_by_bundle_from_app_store(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    bundle_id = config['as']['bundle_id']
    download_info = subprocess.run(
        ['docker', 'run', 'npinaev/poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_bundle_id',
         f'{bundle_id}'])
    out, err = capfd.readouterr()
    assert "INFO Successfully logged in" in out
    assert "INFO Trying to find app in App Store with bundle id ru.gazprombank.ios.mobilebank" in out
    assert "Successfully found application by bundle id (ru.gazprombank.ios.mobilebank)" in out
    assert "Trying to purchase app with id" in out
    assert "This app was purchased before for" in out
    assert "Downloading app is Газпромбанк" in out
    assert "INFO Your application was downloaded!" in out


def test_pypi_download_app_by_id_from_app_store(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    app_id = config['as']['app_id']
    download_info = subprocess.run(
        ['poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_app_id',
         f'{app_id}'])
    out, err = capfd.readouterr()
    assert download_info.returncode == 0
    assert "INFO Successfully logged in" in out
    assert "Trying to purchase app with id" in out
    assert "This app was purchased before for" in out
    assert "INFO Downloading app is Ростелеком" in out
    assert "INFO Creating iTunesMetadata.plist with metadata info" in out
    assert "INFO Your application was downloaded!" in out


def test_docker_download_app_by_id_from_app_store(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    app_id = config['as']['app_id']
    download_info = subprocess.run(
        ['docker', 'run', 'npinaev/poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_app_id',
         f'{app_id}'])
    out, err = capfd.readouterr()
    assert "INFO Successfully logged in" in out
    assert "Trying to purchase app with id" in out
    assert "This app was purchased before for" in out
    assert "INFO Downloading app is Ростелеком" in out
    assert "INFO Creating iTunesMetadata.plist with metadata info" in out
    assert "INFO Your application was downloaded!" in out


def test_pypi_download_paid_app_from_app_store(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    paid_app_id = config['as']['paid_app_id']
    download_paid_app_info = subprocess.run(
        ['poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_app_id',
         f'{paid_app_id}'])
    out, err = capfd.readouterr()
    assert download_paid_app_info.returncode == 1
    assert "'NoneType' object has no attribute 'dialogId'" in err


def test_docker_download_paid_app_from_app_store(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    paid_app_id = config['as']['paid_app_id']
    download_paid_app_info = subprocess.run(
        ['docker', 'run', 'npinaev/poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_app_id',
         f'{paid_app_id}'])
    out, err = capfd.readouterr()
    assert download_paid_app_info.returncode == 1
    assert "'NoneType' object has no attribute 'dialogId'" in err


def test_stability_testing_for_appstore_logins(capfd):
    apple_id = config['as']['apple_id']
    password2FA = config['as']['password2FA']
    bundle_id = config['as']['bundle_id']
    t_end = time.time() + 60
    while time.time() < t_end:
        lookup_info = subprocess.run(
            ['poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
             f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_bundle_id',
             f'{bundle_id}', '--lookup'])
        out, err = capfd.readouterr()
        assert lookup_info.returncode == 0
        assert "INFO Successfully logged in" in out
        assert "INFO Successfully found application by bundle id (ru.gazprombank.ios.mobilebank) with name:" in out
        assert "app_id: 1406492297" in out


def test_load_testing_google_play_download(capfd):
    gsfid = int(config['gp']['gsfid'])
    authSubToken = config['gp']['authSubToken']
    for package_name in PACKAGE_NAMES:
        download_from_gp = subprocess.run(
            ['poly_app_downloader', '--distribution_system', 'google_play', '--google_play_package_name',
             f'{package_name}', '--google_play_gsfid', f'{gsfid}', '--google_play_auth_token',
             f'{authSubToken}'])
        out, err = capfd.readouterr()
        assert download_from_gp.returncode == 0
        assert "INFO Your application was downloaded!" in out
        assert "INFO Google Play - Logging in with gsfid and auth token" in out
        assert "INFO Google Play - Successfully logged in Play Store" in out
        assert f'{package_name}' in out
        assert "INFO Your application was downloaded!" in out
