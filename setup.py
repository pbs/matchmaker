#!/usr/bin/env python
from setuptools import setup, find_packages

dependencies = [
	'requests==2.20.0',
	'python-memcached==1.5.3'
]

setup (
	name = 'matchmaker',
	version = '0.1',
	author = 'Becky Brown',
	author_email = 'rbrown4@mail.umw.edu',
	packages = find_packages(),
		include_package_data = True,
	url = 'https://github.com/pbs/matchmaker',
	description = 'A means to connect a user\'s MyPBS account to his OTT devices (ATV, Roku, GoogleTV)',
	long_description = open('README.md').read(),
	install_requires = dependencies
)
