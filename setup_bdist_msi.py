#!/usr/bin/env python

import os
import re
import sys

from setuptools import setup
from cx_Freeze import setup, Executable  # noqa re-import setup

# Check for Windows MSI Setup
if "bdist_msi" not in sys.argv:  # or len(sys.argv) != 2:
    raise RuntimeError(
        "This setup.py variant is only for creating 'bdist_msi' targets: {}\n"
        "Example `{} bdist_msi`".format(sys.argv, sys.argv[0])
    )

from yabs_test import __version__

org_version = __version__

# # Get version number without importing
# # In this case, we need special code, because
# #     from yabs_test import __version__
# # we have a /src folder:
# # See https://packaging.python.org/en/latest/guides/single-sourcing-package-version/

# def read_version(rel_path):
#     here = os.path.abspath(os.path.dirname(__file__))
#     with open(os.path.join(here, rel_path), "r") as fp:
#         for line in fp.read().splitlines():
#             if line.startswith("__version__"):
#                 delim = '"' if '"' in line else "'"
#                 return line.split(delim)[1]
#     raise RuntimeError("Unable to find version string.")

# org_version = read_version("yabs_test/__init__.py")

# # 'setup.py upload' fails on Vista, because .pypirc is searched on 'HOME' path
# if "HOME" not in os.environ and "HOMEPATH" in os.environ:
#     os.environ.setdefault("HOME", os.environ.get("HOMEPATH", ""))
#     print("Initializing HOME environment variable to '{}'".format(os.environ["HOME"]))

# Since we included pywin32 extensions, cx_Freeze tries to create a
# version resource. This only supports the 'a.b.c[.d]' format.
# Our version has either the for '1.2.3' or '1.2.3-a1'
major, minor, patch = org_version.split(".", 3)
major = int(major)
minor = int(minor)

# We have a pre-release version, e.g. '1.2.3-a1'.
# This is presumably a post-release increment after '1.2.2' release.
# It must NOT be converted to '1.2.3.1', since that would be *greater*
# than '1.2.3', which is not even released yet.
#
# Approach 1: allow_post_releases = False
#     We cannot guarantee that '1.2.2.1' is correct either, so for
#     pre-releases we assume '0.0.0.0':
#
# Approach 2: allow_post_releases = True
#     '1.2.3-a1' was presumably a post-release increment after '1.2.2',
#     so assume '1.2.2.1'

allow_post_releases = False

if "-" in patch:
    patch, alpha = patch.split("-", 1)
    patch = int(patch)
    # Remove leading letters
    alpha = re.sub("^[a-zA-Z]+", "", alpha)
    alpha = int(alpha)
    if patch >= 1 and allow_post_releases:
        patch -= 1  # 1.2.3-a1 => 1.2.2.1
    else:
        # may be 1.2.0-a1 or 2.0.0-a1: we don't know what the previous release was
        major = minor = patch = alpha = 0
else:
    patch, alpha = patch.split("-", 1)
    patch = patch.split("-", 1)[0]
    patch = int(patch)
    alpha = 0

version = f"{major}.{minor}.{patch}.{alpha}"
print(f"Package version {org_version}: using installer version {version}")

try:
    readme = open("README.md", "rt").read()
except IOError:
    readme = "(readme not found. Running from tox/setup.py test?)"

# NOTE: Only need to list requirements that are not discoverable by scanning
#       the main package. For example due to dynamic or optional imports.
# Also, cx_Freeze may have difficulties with packages listed here, e.g. PyYAML:
#    https://github.com/marcelotduarte/cx_Freeze/issues/1541
install_requires = []
setup_requires = install_requires
tests_require = []

executables = [
    Executable(
        script="yabs_test/main.py",
        base=None,
        # base="Win32GUI",
        target_name="yabs_test.exe",
        # icon="docs/logo.ico",
        shortcut_name="yabs_test",
        copyright="(c) 2012-2022 Martin Wendt",
        # trademarks="...",
    )
]

# See https://cx-freeze.readthedocs.io/en/latest/distutils.html#build-exe
build_exe_options = {
    # "init_script": "Console",
    "includes": install_requires,
    "packages": ["keyring.backends"],  # loaded dynamically
    "constants": "BUILD_COPYRIGHT='(c) 2012-2022 Martin Wendt'",
}

# See https://cx-freeze.readthedocs.io/en/latest/distutils.html#bdist-msi
bdist_msi_options = {
    "upgrade_code": "{F0C1843D-F39F-4848-9E98-085C536200C0}",
    "add_to_path": True,
    # "install_icon": "docs/logo.ico",
    # "all_users": True,
    # "summary_data": {"author": "Martin Wendt"},
}


setup(
    name="yabs_test",
    version=version,
    author="Martin Wendt",
    author_email="yabs@wwwendt.de",
    # copyright="(c) 2012-2022 Martin Wendt",
    maintainer="Martin Wendt",
    maintainer_email="yabs@wwwendt.de",
    url="https://github.com/mar10/yabs_test",
    description="Dummy application to test release workflows with mar10/yabs.",
    long_description=readme,
    long_description_content_type="text/markdown",
    # Not required for this build-only setup config:
    classifiers=[],
    keywords="test, temporary, setup, yabs",
    license="The MIT License",
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    # package_dir="src",
    packages=["yabs_test"],
    zip_safe=False,
    extras_require={},
    # cmdclass={"test": ToxCommand, "sphinx": SphinxCommand},
    entry_points={"console_scripts": ["pyftpsync=yabs_test.main:run"]},
    executables=executables,
    options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
)
