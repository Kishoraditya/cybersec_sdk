# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/


# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='cyberguard-sdk',
    version='1.0.0',
    packages=find_packages(),
    install_requires=requirements,
    author='Kishoraditya',
    author_email='kishoradityasc@gmail.com',
    description='Open source, AI-driven cybersecurity SDK for system analysis, actor identification, autonomous threat detection, analysis and mitigation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kishoraditya/cyberguard-sdk',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'License :: OSI Approved :: Creative Commons Attribution-NonCommercial 4.0 International License',  
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cyberguard=cybersec_sdk.example_usage:main',
        ],
    },
)
