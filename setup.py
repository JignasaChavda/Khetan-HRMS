from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in khetanhrms/__init__.py
from khetanhrms import __version__ as version

setup(
	name="khetanhrms",
	version=version,
	description="Khetan HRMS",
	author="Jignasha",
	author_email="jignasha@sanskartechnolab.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
