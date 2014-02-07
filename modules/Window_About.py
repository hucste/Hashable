#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

#
## Authors informations
#
# @author: HUC Stéphane
# @email: <devs@stephane-huc.net>
# @url: http://stephane-huc.net
#
# @license : GNU/GPL 3
#

import gtk, logging

class Window_About:
	'Display a window about'

	def __init__(self, array):

		self.dic = array;

	def run(self):
		self.log.info('=> Displaying Window About')

		about = gtk.AboutDialog()
		about.set_logo_icon_name('help-about')
		about.set_property('icon-name','help-about')

		for d in self.dic:
			if d == 'icon':
				setattr(self, d, self.dic[d])
			else:
				getattr(about, 'set_%s' % d )( self.dic[ d ] )

			self.log.debug('Create methode set_%s for gtk.AboutDialog...' % d)

		#about.set_icon_from_file(self.icon)
		about.run()
		about.destroy()

		self.log.info('=> Destroying Window About')

	def set_debug(self, entry):
		self.debug = bool( entry )

	def set_log(self, entry):
		self.log = entry
