import os
from distutils.command.build import build

from setuptools import find_packages, setup
from django.core import management

try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except:
    long_description = None


setup(
    name="barman-stocks",
    version=0.1,
    description="Add stocks for products",
    long_description=long_description,
    author="Yoann Pietri",
    author_email="me@nanoy.fr",
    url="https://github.com/barmanaginn/barman-stocks",
    license="GPLv3",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
[barman.plugin]
barman_stocks=barman_stocks:BarmanPluginMeta
""",
)
