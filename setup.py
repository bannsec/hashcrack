# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os, sys, ast

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "hashcrack", "version.py"), "r") as f:
    exec(f.read())

#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()
long_description = "See website for more info."

setup(
    name='hashcrack',
    version=version,
    description='Menu for cracking hashes.',
    long_description=long_description,
    url='https://github.com/bannsec/hashcrack',
    author='Michael Bann',
    author_email='self@bannsecurity.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console'
    ],
    keywords='password hashcat cracking',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['prettytable', 'appdirs', 'prompt-toolkit', 'hashid', 'hashcat-beta'],
    extras_require={
        'dev': ['ipython','twine','pytest','python-coveralls','coverage==4.5.4','pytest-cov','pytest-xdist','sphinxcontrib-napoleon', 'sphinx_rtd_theme','sphinx-autodoc-typehints'],
    },
    entry_points={
        'console_scripts': [
            'hashcrack = hashcrack.cli:main',
        ],
    },
    include_package_data = True,
)

