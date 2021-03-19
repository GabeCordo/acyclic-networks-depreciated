from setuptools import setup, find_packages

with open("README.md", "r") as fh:
	readme_description = fh.read()

longDescription = 'A (S)ecure (C)ommunication and (M)essaging (S)ervice is a lightweight tool for providing encrypted client-server messaging with path-routing features.'

setup(
	name = 'quickscms',
	packages = find_packages(),
	version = '1.1.6',
	licence = 'MIT',
	description = longDescription,
	author = 'Gabriel Cordovado',
	author_email = 'gabriel.cordovado@icloud.com',
	long_description = readme_description,
	long_description_content_type = 'text/markdown',
	url ='https://github.com/GabeCordo/python-node-tor',
	download_url = 'https://github.com/GabeCordo/python_node_tor/archive/v_1.1.5.7.tar.gz',
	keywords = ['TOR', 'SOCKETS', 'SECURITY', 'ENCRYPTION'],
	install_requires = [
		'cffi',
		'pycryptodomex',
		'pyfiglet',
		'clint',
		'pyyaml'
	],
	classifiers = [
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
	python_requires = '>=3.4'
)
