from setuptools import find_packages, setup

from mdast_cli.helpers.const import TAG

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="poly_app_downloader",

    version=TAG,

    author="npinaev",
    description="app_downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/npinaev/poly_app_downloader",
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['device.properties']},
    install_requires=[
        'beautifulsoup4==4.10.0',
        'cachetools==5.0.0',
        'certifi==2021.10.8',
        'cffi==1.15.0',
        'chardet==3.0.4',
        'charset-normalizer==2.0.12',
        'cryptography==36.0.1',
        'google==3.0.0',
        'google-api-core==2.7.0',
        'google-api-python-client==2.39.0',
        'google-auth==2.6.0',
        'google-auth-httplib2==0.1.0',
        'googleapis-common-protos==1.55.0',
        'httplib2==0.20.4',
        'idna==2.7',
        'protobuf==3.19.4',
        'pyasn1==0.4.8',
        'pyasn1-modules==0.2.8',
        'pycparser==2.21',
        'pyparsing==3.0.7',
        'requests==2.27.1',
        'rsa==4.8',
        'six==1.16.0',
        'soupsieve==2.3.1',
        'uritemplate==4.1.1',
        'urllib3==1.26.0',
        'pytest==7.1.2'
    ],
    entry_points={
        'console_scripts': [
            'poly_app_downloader=mdast_cli.mdast_scan:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)
