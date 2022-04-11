"""setuptools based setup script for biotools package

This script uses setuptools which is standard mechanism
for installing python package. If you downloaded and 
decompressed the 'biotools' package source code, the simplest
installation is just typing the command::
    
    python setup.py install

For more information, see the installation part of the github
repository.

    https://github.com/Beomman-Han/biotools

Or, if all trials fail, feel free to write ask for help.

    qjaaks6378@gmail.com 
"""

from setuptools import setup

__author__ = 'Beomman Han'
__author_email__ = 'qjaaks6378@gmail.com'
__version__ = 'undefined'

for line in open('__init__.py'):
    if line.startswith('__version__'):
        exec(line.strip())
    if line.startswith('__author__'):
        exec(line.strip())
    if line.startswith('__author_email__'):
        exec(line.strip())

setup(
    name='biotools',
    version = __version__,
    python_requires='>=3.7',
    description='first version of biotools package',
    author='Beomman Han',
    author_email='qjaaks6378@gmail.com',
    #packages=['FASTA', 'VCF'],
    packages=['BI',
              'BI.FASTA',
              'BI.VCF'],
    #install_requires=['gzip', 're', 'json']
)