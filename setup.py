#!/usr/bin/env python
import codecs
import os.path
import re

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [
    'click==8.1.3',
    'python-dotenv==0.20.0',
    'PyYAML==6.0',
]


setup_options = dict(
    name='dotenv2k8s',
    version=find_version("dotenv2k8s", "__init__.py"),
    description='Command Line to export dotenv files to Kubernetes Secrets declarative manifests',
    long_description=read('README.rst'),
    long_description_content_type="text/x-rst",
    author='juliocsmelo@gmail.com',
    url='https://github.com/juliosmelo/dotenv2k8s',
    scripts=['bin/dotenv2k8s',],
    packages=find_packages(exclude=['tests*']),
    install_requires=install_requires,
    extras_require={},
    license="Apache License 2.0",
    python_requires=">= 3.7",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        'Source': 'https://github.com/juliosmelo/dotenv2k8s',
    },
)

setup(**setup_options)
