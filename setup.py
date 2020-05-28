from setuptools import setup, find_packages

with open("README.md", "r") as fh:
	readme_description = fh.read()

longDescription = 'A mid-weight framework for replicating tor entry, relay and exit nodes. Developed for programmers looking to provide highly-secure messaging/file transfer applications. Equipt with end-to-end encryption and anonymous server meshing.'

setup(
	name = 'pynodetor',
	packages = find_packages(),
	version = '1.1.5.7',
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
		'pycryptodomex'
	],
	classifiers = [
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
	python_requries = '>=3.4'
)
