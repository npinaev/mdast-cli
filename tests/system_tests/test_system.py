import math
import subprocess
import sys

import requests
from pytest_testconfig import config

from mdast_cli.helpers.const import TAG


# System tests
def test_install_pypi_package(capfd):
    install_pypi = subprocess.run(
        ['pip', 'install', 'poly_app_downloader', '-U'])
    out, err = capfd.readouterr()
    assert install_pypi.returncode == 0
    assert ("Requirement already satisfied" in out or "Successfully installed" in out)
    assert TAG in out


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
    apple_id = int(config['as']['apple_id'])
    password2FA = config['as']['password2FA']
    bundle_id = config['as']['bundle_id']
    lookup_info = subprocess.run(
        ['poly_app_downloader', '--distribution_system', 'appstore', '--appstore_apple_id',
         f'{apple_id}', '--appstore_password2FA', f'{password2FA}', '--appstore_bundle_id',
         f'{bundle_id}', '--lookup'])
    out, err = capfd.readouterr()
    assert download_from_gp.returncode == 0
    assert "Item found" in out

