"""Project: Phi_K - correlation coefficient package

Created: 2018/11/13

Description:
    setup script to install Phi_K correlation package.

Authors:
    KPMG Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

from setuptools import find_packages
from setuptools import setup

NAME = 'phik'

MAJOR = 0
REVISION = 9
PATCH = 11
DEV = False

# note: also update README.rst

VERSION = '{major}.{revision}.{patch}'.format(major=MAJOR, revision=REVISION, patch=PATCH)
FULL_VERSION = VERSION
if DEV:
    FULL_VERSION += '.dev'

TEST_REQUIREMENTS = ['pytest>=4.0.2',
                     'pytest-pylint>=0.13.0',
                     'nbconvert>=5.3.1',
                     'jupyter_client>=5.2.3',
                     ]

REQUIREMENTS = [
    'numpy>=1.15.4',
    'scipy>=1.1.0',
    'pandas>=0.23.4',
    'matplotlib>=2.2.3',
    'numba>=0.38.1',
    'joblib>=0.14.1'
    ]

if DEV:
    REQUIREMENTS += TEST_REQUIREMENTS

CMD_CLASS = dict()
COMMAND_OPTIONS = dict()

EXCLUDE_PACKAGES = []
EXTERNAL_MODULES = []

with open("README.rst", "r") as fh:
    long_description = fh.read()


def write_version_py(filename: str = 'python/phik/version.py') -> None:
    """Write package version to version.py.

    This will ensure that the version in version.py is in sync with us.

    :param filename: The version.py to write too.
    :type filename: str
    :return:
    :rtype: None
    """
    # Do not modify the indentation of version_str!
    version_str = """\"\"\"THIS FILE IS AUTO-GENERATED BY PHIK SETUP.PY.\"\"\"

name = '{name!s}'
version = '{version!s}'
full_version = '{full_version!s}'
release = {is_release!s}
"""

    version_file = open(filename, 'w')
    try:
        version_file.write(version_str.format(name=NAME.lower(),
                                              version=VERSION,
                                              full_version=FULL_VERSION,
                                              is_release=not DEV))
    finally:
        version_file.close()


def setup_package() -> None:
    """The main setup method.

    It is responsible for setting up and installing the package.

    :return:
    :rtype: None
    """
    write_version_py()

    setup(name=NAME,
          version=FULL_VERSION,
          url='http://phik.rtfd.io',
          license='',
          author='KPMG N.V. The Netherlands',
          author_email='kave@kpmg.com',
          description="Phi_K correlation analyzer library",
          python_requires='>=3.5',
          package_dir={'': 'python'},
          packages=find_packages(where='python', exclude=EXCLUDE_PACKAGES),
          # Setuptools requires that package data are located inside the package.
          # This is a feature and not a bug, see
          # http://setuptools.readthedocs.io/en/latest/setuptools.html#non-package-data-files
          package_data={
              NAME.lower(): ['data/*', 'notebooks/phik_tutorial*.ipynb']
          },
          install_requires=REQUIREMENTS,
          tests_require=TEST_REQUIREMENTS,
          ext_modules=EXTERNAL_MODULES,
          cmdclass=CMD_CLASS,
          command_options=COMMAND_OPTIONS,
          classifiers=(
              "Programming Language :: Python :: 3",
              "Operating System :: OS Independent",
          ),
          # The following 'creates' executable scripts for *nix and Windows.
          # As an added bonus the Windows scripts will auto-magically
          # get a .exe extension.
          #
          # phik_trial: test application to let loose on tests. This is just a wrapper around pytest.
          entry_points={
              'console_scripts': [
                  'phik_trial = phik.entry_points:phik_trial'
              ]
          }
          )


if __name__ == '__main__':
    setup_package()
