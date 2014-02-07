#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import glob, os

dirname = os.path.dirname(os.path.abspath(__file__))

files = glob.glob( dirname + '/*.py' )

l = []

me = os.path.basename(__file__)

for f in files:
	(path, file) = os.path.split( f )
	if os.path.isfile( f ) and file <> me:
		(name, ext) = os.path.splitext( file )
		if name <> '__init__' and not name in l :
			l.append( name )

__all__ = l
