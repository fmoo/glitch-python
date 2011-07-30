#!/usr/bin/env python

from distutils.core import setup

setup(name='glitch-python',
      version='0.2',
      description='Python API bindings for the game glitch',
      author='Peter Ruibal',
      author_email='ruibalp@gmail.com',
      url='http://github.com/fmoo/glitch-python',
      packages=['glitch'],
      provides=['glitch'],
      requires=['requests'],
)
