"""
StratoDem Analytics : setup
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

December 26, 2018
"""

import os
from setuptools import setup


this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='strato_query',
    version='3.10.1',
    author='Michael Clawar, Raaid Arshad, Eric Linden',
    author_email='tech@stratodem.com',
    packages=[
        'strato_query',
    ],
    license='MIT',
    description='StratoDem Analytics API tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/StratoDem/strato-query',
)
