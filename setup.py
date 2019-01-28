"""
StratoDem Analytics : setup
Principal Author(s) : Eric Linden
Secondary Author(s) :
Description :

Notes :

December 26, 2018
"""

from setuptools import setup

setup(
    name='strato_query',
    version='2.6.0',
    author='Michael Clawar, Raaid Arshad, Eric Linden',
    author_email='tech@stratodem.com',
    packages=[
        'strato_query',
        'strato_query.core',
    ],
    license='MIT',
    description='StratoDem DB API tools',
    url='https://github.com/StratoDem/strato-query',
)
