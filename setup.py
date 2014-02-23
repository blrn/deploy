from setuptools import setup, find_packages
import sys, os
setup(name="deploy",
	version="0.0.1",
	description="Python CLI application that transfers files to a remote web server.",
	packages=find_packages(),
	package_data = {
		'deploy' : ['templates/*.json']
	},
	zip_safe=False,
	entry_points = {
		'console_scripts': [
			'deploy = deploy.main:main'
		]
	}
)
