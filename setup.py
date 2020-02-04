#!/usr/bin/env python
from setuptools import find_packages, setup


def readfile(path):
    with open(path) as fd:
        return fd.read()


setup(
    name='django-async-messages-redux',
    version='0.5.0',
    url='https://github.com/maurizi/django-async-messages',
    author='Michael Maurizi',
    author_email='michael@maurizi.org',
    description="Send asynchronous messages to users (eg from offline scripts). Useful for integration with Celery.",
    long_description=readfile('README.rst'),
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'django>=1.11,<3.1'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
)
