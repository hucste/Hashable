# A very simple setup script to create 1 executables with py2exe
# Run in comand line python setup.py py2exe -i qt,sip -b 1
import os
from distutils.core import setup
import py2exe

setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    author = 'Stephane HUC',
    description = 'Software to calculate or control checksum file',
    name = 'Hashable Calculator',
	version = file(os.getcwd() + '/VERSION').read(),

    # targets to build
    # console = ['Hashable.py'], # pour un mode console
    windows = [
		{
			'icone_resources':	[ (1, '') ],
			'script':	'Hashable.py',
		}
	],
)
