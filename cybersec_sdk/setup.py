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
