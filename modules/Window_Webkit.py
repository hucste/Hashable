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

#
## LIBRARIES IMPORT
#

import gobject
import gtk
import os
import sys

try:
	#from gi.repository import WebKit as webkit
	#from gi.repository import Gtk as gtk
	import webkit
except:
	print 'Cant import webkit'
	sys.exit(1)

class Window_Webkit:
	'Building Window with webkit technology'

	def __init__(self, init):

		for i in init:
			setattr(self, i, init[i])

		self.log.info('=> Displaying Window Webkit')

	def add_submenu(self):
		# add submenu
		submenu = gtk.Menu()

		for i in self.actions:
			item = gtk.MenuItem(i)
			submenu.append(item)
			#item.connect('activate', self.on_subitem, i)
			item.show()

		return submenu
		#self.itemNew.set_submenu(self.submenuNew)

	def create_gui(self):
		self.gui = webkit.WebView()
		#.connect("document-load-finished", document_load_finished_cb)
		#.connect("navigation-policy-decision-requested", nav_request_cb)
		self.gui.connect('populate-popup', self.populate_popup)
		#.connect("resource-request-starting", resource_request_starting_cb)
		self.gui.connect('title-changed', self.title_changed)
		self.gui.open(os.path.join(self.dir, self.libgui, 'index.html'))
		self.gui.set_transparent(True)
		#self.gui.load_string(HTML, 'text/html', "utf-8", '')

	def create_status_icon(self):
		self.statusIcon = gtk.StatusIcon()
		self.statusIcon.connect('activate', self.on_click_statusIcon)
		self.statusIcon.connect('popup-menu', self.on_menu_statusIcon)
		self.statusIcon.set_from_icon_name('accessories-calculator')
		self.statusIcon.set_tooltip(self.title['mainWindow'])
		self.statusIcon.set_visible(True)

	def create_window(self):
		self.mainWindow = gtk.Window()

		self.scrollWindow = gtk.ScrolledWindow()
		self.scrollWindow.add(self.gui)
		self.mainWindow.add(self.scrollWindow)

		self.mainWindow.connect('delete_event', gtk.main_quit)
		self.mainWindow.connect('destroy', self.destroy_app)
		self.mainWindow.set_border_width(0)
		self.mainWindow.set_property('icon-name','accessories-calculator')
		self.mainWindow.set_opacity(0.95)
		self.mainWindow.set_resizable(False)
		self.mainWindow.set_size_request(400, 300)
		self.mainWindow.set_title(self.title['mainWindow'])

		# add accelerator group
		self.ag = gtk.AccelGroup()
		self.mainWindow.add_accel_group(self.ag)

	def destroy_app(self):
		gtk.main_quit()

	def execute(self, script):
		self.gui.execute_script(script)

	def main(self):
		gtk.main()

	def on_click_statusIcon(self, widget):
		if self.mainWindow.get_property('visible'):
			self.mainWindow.hide()
		else:
			self.mainWindow.show()

	def on_menu_statusIcon(self, status_icon, button, activate_time):
		self.menuSI = gtk.Menu()
		self.itemQuitSI = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		self.itemQuitSI.add_accelerator('activate', self.ag, gtk.keysyms.Q, gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
		self.itemQuitSI.connect('activate', gtk.main_quit)
		self.menuSI.append(self.itemQuitSI)
		self.menuSI.popup(None, None, gtk.status_icon_position_menu, button, activate_time, status_icon)
		self.menuSI.show_all()

	def populate_popup(self, view, menu):
		sep1 = gtk.SeparatorMenuItem()
		menu.append(sep1)

		self.itemNewPop = gtk.ImageMenuItem(gtk.STOCK_NEW)
		#self.itemNewPop.connect('activate', '')
		self.itemNewPop.set_submenu(self.add_submenu())
		menu.append(self.itemNewPop)

		sep2 = gtk.SeparatorMenuItem()
		menu.append(sep2)

		self.itemQuitPop = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		self.itemQuitPop.connect('activate', gtk.main_quit)
		menu.append(self.itemQuitPop)

		menu.show_all()
		return False

	def run(self):
		self.create_gui()
		self.create_status_icon()
		self.create_window()

		self.mainWindow.show_all()

	def title_changed(self,  widget, frame, title):
		#getattr(self, 'echo', title)
		#print('message', title)
		self.execute('echo("%s")' % title)

