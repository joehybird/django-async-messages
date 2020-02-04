#!/usr/bin/env python
from setuptools import find_packages, setup

setup(name='django-async-messages-redux',
      version='0.5.0',
      url='https://github.com/maurizi/django-async-messages',
      author='Michael Maurizi',
      author_email='michael@maurizi.org',
      description="Send asynchronous messages to users (eg from offline scripts). Useful for integration with Celery.",
      long_description=open('README.rst').read(),
      packages=find_packages(exclude=['tests']),
      install_requires=['django>=1.11'],
      )
