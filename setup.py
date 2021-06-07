# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in pav_beneficiary/__init__.py
from pav_beneficiary import __version__ as version

setup(
	name='pav_beneficiary',
	version=version,
	description='PAV Beneficiary',
	author='Partner Consulting Solutions',
	author_email='t.azzan@partner-cons.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
