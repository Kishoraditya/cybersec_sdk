# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/


# setup.py

from setuptools import setup, find_packages

setup(
    name='cybersec_sdk',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'networkx',
        'pyyaml'
    ],
    author='OpenAI Assistant',
    description='An open-source cybersecurity SDK for system analysis and actor identification.',
    url='https://github.com/kishoraditya/cybersec_sdk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
