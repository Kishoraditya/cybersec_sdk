# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/


# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
#with open("requirements.txt") as f:
#    requirements = f.read().splitlines()

setup(
    name='cyberguard-sdk',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'altair==4.2.2',
        'annotated-types==0.7.0',
        'anyio==4.6.0',
        'asttokens==2.4.1',
        'attrs==24.2.0',
        'blinker==1.8.2',
        'cachetools==5.5.0',
        'certifi==2024.8.30',
        'charset-normalizer==3.3.2',
        'click==8.1.7',
        'colorama==0.4.6',
        'contourpy==1.3.0',
        'cycler==0.12.1',
        'decorator==5.1.1',
        'distro==1.9.0',
        'entrypoints==0.4',
        'exceptiongroup==1.2.2',
        'executing==2.1.0',
        'fonttools==4.54.1',
        'gitdb==4.0.11',
        'GitPython==3.1.43',
        'google-ai-generativelanguage==0.6.10',
        'google-api-core==2.20.0',
        'google-api-python-client==2.147.0',
        'google-auth==2.35.0',
        'google-auth-httplib2==0.2.0',
        'google-generativeai==0.8.2',
        'googleapis-common-protos==1.65.0',
        'grpcio==1.66.2',
        'grpcio-status==1.44.0',
        'h11==0.14.0',
        'httpcore==1.0.5',
        'httplib2==0.22.0',
        'httpx==0.27.2',
        'idna==3.10',
        'importlib_metadata==8.5.0',
        'importlib_resources==6.4.5',
        'ipython==8.18.1',
        'jedi==0.19.1',
        'Jinja2==3.1.4',
        'jiter==0.5.0',
        'joblib==1.4.2',
        'jsonpickle==3.3.0',
        'jsonschema==4.23.0',
        'jsonschema-specifications==2023.12.1',
        'kiwisolver==1.4.7',
        'markdown-it-py==3.0.0',
        'MarkupSafe==2.1.5',
        'matplotlib==3.9.2',
        'matplotlib-inline==0.1.7',
        'mdurl==0.1.2',
        'narwhals==1.8.4',
        'neo4j==5.25.0',
        'networkx==3.2.1',
        'numpy==2.0.2',
        'openai==1.50.2',
        'packaging==24.1',
        'pandas==2.2.3',
        'parso==0.8.4',
        'pillow==10.4.0',
        'prompt_toolkit==3.0.48',
        'proto-plus==1.24.0',
        'protobuf==3.20.3',
        'psutil==6.0.0',
        'pure_eval==0.2.3',
        'pyarrow==17.0.0',
        'pyasn1==0.6.1',
        'pyasn1_modules==0.4.1',
        'pydantic==2.9.2',
        'pydantic_core==2.23.4',
        'pydeck==0.9.1',
        'Pygments==2.18.0',
        'Pympler==1.1',
        'pyparsing==3.1.4',
        'python-dateutil==2.9.0.post0',
        'pytz==2024.2',
        'pyvis==0.3.2',
        'pywin32==306',
        'PyYAML==6.0.2',
        'referencing==0.35.1',
        'requests==2.32.3',
        'rich==13.8.1',
        'rpds-py==0.20.0',
        'rsa==4.9',
        'scikit-learn==1.5.2',
        'scipy==1.13.1',
        'seaborn==0.13.2',
        'semver==3.0.2',
        'six==1.16.0',
        'smmap==5.0.1',
        'sniffio==1.3.1',
        'stack-data==0.6.3',
        'streamlit==1.12.0',
        'threadpoolctl==3.5.0',
        'toml==0.10.2',
        'toolz==0.12.1',
        'tornado==6.4.1',
        'tqdm==4.66.5',
        'traitlets==5.14.3',
        'typing==3.7.4.3',
        'typing_extensions==4.12.2',
        'tzdata==2024.2',
        'tzlocal==5.2',
        'uritemplate==4.1.1',
        'urllib3==2.2.3',
        'validators==0.34.0',
        'watchdog==5.0.3',
        'wcwidth==0.2.13',
        'zipp==3.20.2',
    ],
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
        'License :: Other/Proprietary License',  
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    license='CC BY-NC 4.0',
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cyberguard=cybersec_sdk.example_usage:main',
        ],
    },
)
