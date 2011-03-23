#!/usr/bin/env python

from distutils.core import setup
import os.path, sys


def read(filename):
    return open(os.path.join(sys.path[0], filename)).read()


VERSION     = '0.1'
DESCRIPTION = 'Python Spotify API'

setup(
    name='spotify',
    version=VERSION,
    description=DESCRIPTION,
    long_description=read('README'),
    license='GPL',
    author='Nauzet Hernandez',
    author_email='nauzethc@gmail.com',
    url='http://code.google.com/p/python-spotify/',
    keywords='spotify api dbus command',
    packages=['spotify'],
    platforms=['linux'],
    classifiers=[
        "Development Status :: Alpha",
        "Enviroment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)