import setuptools

with open("README.md", "r") as fh:
	readme_description = fh.read()

setuptools.setup(
	name = 'pynodetor',
	version = '1.0',
	description = 'A mid-weight framework for replicating tor entry, relay and exit nodes. Developed for programmers looking to provide highly-secure messaging/file transfer applications. Equipt with end-to-end encryption and anonymous server meshing.',
	author = 'Gabriel Cordovado',
	author_email = 'gabriel.cordovado@icloud.com',
	long_description = readme_description,
	long_description_content_type = 'text/markdown',
	url ='https://github.com/GabeCordo/python-node-tor',
	packages = setuptools.find_packages(),
	classifiers = [
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requries = '>=3.4',
)