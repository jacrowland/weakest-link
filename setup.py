# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='The Weakest Link',
    version='0.1.0',
    description='CLI trivia game show based off The Weakest Link TV show',
    long_description=readme,
    author='Jacob Rowland',
    author_email='',
    url='https://github.com/jacrowland/weakest-link',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

