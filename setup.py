import os

import tomli
from setuptools import setup

# Read version from pyproject.toml
with open("pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)
    version = pyproject["tool"]["poetry"]["version"]

# Update __version__.py
version_file = os.path.join("xontrib_1password", "__version__.py")
with open(version_file, "w") as f:
    f.write('"""Version information for xontrib-1password."""\n\n')
    f.write(f'__version__ = "{version}"\n')

setup()
