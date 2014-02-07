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

import gettext
import gtk
import os

try:
    from modules import Window_FileChooser
    Window_FileChooser = Window_FileChooser.Window_FileChooser
except:
    print 'Cant import modules Window_FileChooser onto Window_Message'
    sys.exit(1)

class Window_Message:
    'Display a window message'

    def __init__(self, array):
        self.dic = array

    def init_vars(self):
        for d in self.dic:
            setattr(self, d, self.dic[ d ])

            self.log.debug('Window Message: Create variable self.%s needed...' % d)

    def run(self):
        self.init_vars()

        self.log.info('=> Displaying Window Message')

        mssg = gtk.MessageDialog(None, gtk.DIALOG_MODAL, self.flag, self.gtkbtn, self.mssg)

        if self.flag == 'info':
            self.iconName = 'dialog-information'
        else:
            self.iconName = 'dialog-' + self.flag

        mssg.set_property('icon-name',self.iconName)

        if self.gtkbtn == gtk.BUTTONS_YES_NO and self.fileChooser:
            response = mssg.run()

            if response == gtk.RESPONSE_YES:
                array = {
                    'algo': self.algo,
                    'algos': self.algos,
                    'action': gtk.FILE_CHOOSER_ACTION_SAVE,
                    'checksum': self.checksum,
                    'file': os.path.basename(self.file),
                    'title': self.title['window_saving'],
                    'version': self.version,
                }

                WFC = Window_FileChooser(array)
                WFC.set_debug(self.debug)
                WFC.set_log(self.log)
                WFC.set_text(self.text)
                WFC.run()

        else:
            mssg.run()

        mssg.destroy()
        self.log.info('=> Destroying Window Message')

    def set_debug(self, entry):
        self.debug = bool( entry )

    def set_log(self, entry):
        self.log = entry
