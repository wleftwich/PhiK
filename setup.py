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

import os
import sys
import subprocess
from setuptools import find_packages
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11


NAME = 'phik'

MAJOR = 0
REVISION = 11
PATCH = 2
DEV = False

# note: also update README.rst

VERSION = '{major}.{revision}.{patch}'.format(major=MAJOR, revision=REVISION, patch=PATCH)
FULL_VERSION = VERSION
if DEV:
    FULL_VERSION += '.dev'

TEST_REQUIREMENTS = [
    'pytest>=4.0.2',
    'pytest-pylint>=0.13.0',
    'nbconvert>=5.3.1',
    'jupyter_client>=5.2.3',
]

REQUIREMENTS = [
    'numpy>=1.18.0',
    'scipy>=1.5.2',
    'pandas>=0.25.1',
    'matplotlib>=2.2.3',
    'joblib>=0.14.1',
]

EXTRA_REQUIREMENTS = {
    'numba': [
        'numba>=0.38.1',
    ],
}

if DEV:
    REQUIREMENTS += TEST_REQUIREMENTS


# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}

# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cfg = "Debug" if self.debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            "-Dpybind11_DIR={}".format(pybind11.get_cmake_dir()),
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}".format(extdir),
            "-DPYTHON_EXECUTABLE={}".format(sys.executable),
            "-DPHIK_VERSION_INFO={}".format(self.distribution.get_version()),
            "-DCMAKE_BUILD_TYPE={}".format(cfg),  # not used on MSVC, but no harm
        ]
        build_args = []

        if self.compiler.compiler_type != "msvc":
            # Using Ninja-build since it a) is available as a wheel and b)
            # multithreads automatically. MSVC would require all variables be
            # exported for Ninja to pick it up, which is a little tricky to do.
            # Users can override the generator with CMAKE_GENERATOR in CMake
            # 3.15+.
            if not cmake_generator:
                cmake_args += ["-GNinja"]

        else:

            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Specify the arch if using MSVC generator, but only if it doesn't
            # contain a backward-compatibility arch spec already in the
            # generator name.
            if not single_config and not contains_arch:
                cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

            # Multi-config generators have a different way to specify configs
            if not single_config:
                cmake_args += [
                    "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
                ]
                build_args += ["--config", cfg]

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += ["-j{}".format(self.parallel)]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )

COMMAND_OPTIONS = dict()
EXCLUDE_PACKAGES = []
CMD_CLASS = {"build_ext": CMakeBuild}
EXTERNAL_MODULES = [CMakeExtension('phik_simulation_core')]

# read the contents of readme file
with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

def write_version_py(filename: str = 'phik/version.py') -> None:
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

    with open(filename, 'w') as version_file:
        version_file.write(
            version_str.format(name=NAME.lower(), version=VERSION, full_version=FULL_VERSION, is_release=not DEV)
        )



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
          license='Apache-2',
          author='KPMG N.V. The Netherlands',
          author_email='kave@kpmg.com',
          description="Phi_K correlation analyzer library",
          long_description=long_description,
          long_description_content_type="text/x-rst",
          python_requires='>=3.6',
          packages=find_packages(exclude=EXCLUDE_PACKAGES),
          # Setuptools requires that package data are located inside the package.
          # This is a feature and not a bug, see
          # http://setuptools.readthedocs.io/en/latest/setuptools.html#non-package-data-files
          package_data={
              NAME.lower(): [
                'data/*',
                'notebooks/phik_tutorial*.ipynb',
            ]
          },
          include_package_data=True,
          install_requires=REQUIREMENTS,
          extras_require=EXTRA_REQUIREMENTS,
          tests_require=TEST_REQUIREMENTS,
          ext_modules=EXTERNAL_MODULES,
          cmdclass=CMD_CLASS,
          command_options=COMMAND_OPTIONS,
          zip_safe=False,
          classifiers=(
              "Programming Language :: Python :: 3",
              "Operating System :: OS Independent",
              "License :: OSI Approved :: Apache Software License",
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
