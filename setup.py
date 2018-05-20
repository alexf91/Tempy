#!/usr/bin/env python

from setuptools import setup

setup(name='Tempy',
    version='0.1',
    description='Creates files or directories from templates',
    author='Alexander Fasching',
    author_email='fasching.a91@gmail.com',
    maintainer='Alexander Fasching',
    maintainer_email='fasching.a91@gmail.com',
    url='https://github.com/alexf91/Tempy',
    license='GPL',
    packages=['tempy'],
    entry_points={
        'console_scripts': ['tempy = tempy.__main__:main']
    },
    install_requires=[
        'Mako'
    ],
)
