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
import gobject
import gtk
import logging
import os
import pango

try:
    from modules import Window_FileChooser
    Window_FileChooser = Window_FileChooser.Window_FileChooser
except:
    print 'Cant import module Window_FileChooser onto Window_Dialog'
    sys.exit(1)

class Window_Dialog:

    def __init__(self, dic):

        self.dic = dic;

    def get_result(self):
        return self.result

    def init_vars(self):

        for d in self.dic:
            setattr(self, d, self.dic[d])

            self.log.debug('Window Dialog: Create variable self.%s needed...' % d)

        self.pref = dict()

    def out_system(self):
        ''' Define variable out... for output file '''

        setattr(self, 'out',
            file(os.path.join(self.dir, self.dirs[0], 'out')).read() )
        if self.out not in self.outs['index']:
            self.out = 'xml'

    def change_preferences(self, button):
        self.folder = self.comboCurrentDir.get_active_text()
        gui = self.comboLibGui.get_active_text()
        out = self.comboOuts.get_active_text()

        for k, v in enumerate(self.fileChooser['dir']['index']):
            if cmp(self.folder, self.fileChooser['dir'][v]['label']) == 0:
                self.pref['current_folder'] = v

        del(self.folder)

        for k, v in enumerate(self.libguis['index']):
            if cmp(gui, self.libguis[v]['label']) == 0:
                self.pref['gui'] = v

        del(gui)

        for k, v in enumerate(self.outs['index']):
            if cmp(out, self.outs[v]['label']) == 0:
                self.pref['out'] = v

        del(out)

        if self.pref['current_folder'] == None or self.pref['current_folder'] not in self.fileChooser['dir']['index']:
            self.pref['current_folder'] = 'current'

        if self.pref['gui'] == None or self.pref['gui'] not in self.libguis['index']:
            self.pref['gui'] = 'libglade'

        if self.pref['out'] == None or self.pref['out'] not in self.outs['index']:
            self.pref['out'] = 'xml'

        self.out = self.pref['out']

        self.write_file()

    def create_buttons(self):

        if self.action == 'calcul' or self.action == 'calculFolder':
            btnNo = gtk.Button(self.text['btnNo'], gtk.STOCK_NO, False)
            btnYes = gtk.Button(self.text['btnYes'], gtk.STOCK_YES, False)

            btnNo.connect('clicked', self.destroy)
            btnYes.connect('clicked', self.saver)

            self.dialog.action_area.pack_start(btnNo, True, True, 0)
            self.dialog.action_area.pack_end(btnYes, True, True, 1)

        elif self.action == 'controlByFile':
            btnOk = gtk.Button(self.text['btnOk'], gtk.STOCK_OK, False)
            btnOk.connect('clicked', self.destroy)
            self.dialog.action_area.pack_start(btnOk, True, True, 0)

        elif self.action == 'precalcul':
            btnApply = gtk.Button(self.text['btnApply'], gtk.STOCK_YES, False)
            btnCancel = gtk.Button(self.text['btnCancel'], gtk.STOCK_NO, False)

            btnApply.connect('clicked', self.precalcul_yes)
            btnCancel.connect('clicked', self.precalcul_no)

            self.dialog.action_area.pack_start(btnCancel, True, True, 0)
            self.dialog.action_area.pack_start(btnApply, True, True, 1)

        elif self.action == 'pref':
            btnApply = gtk.Button(self.text['btnApply'], gtk.STOCK_APPLY, False)
            #btnCancel = gtk.Button(self.text['btnCancel'], gtk.STOCK_CANCEL, False)
            btnOk = gtk.Button(self.text['btnOk'], gtk.STOCK_CLOSE, False)

            btnApply.connect('clicked', self.change_preferences)
            btnOk.connect('clicked', self.destroy)

            self.dialog.action_area.pack_start(btnApply, True, True, 0)
            #self.dialog.action_area.pack_start(btnCancel, True, True, 1)
            self.dialog.action_area.pack_end(btnOk, True, True, 1)

    def create_view_pref(self):
        self.dialog.set_title(self.title['mainWindow'] + ' - ' +
            self.title['window_dialog_pref'])

        self.hbPref1 = gtk.HBox()
        self.hbPref2 = gtk.HBox()
        self.hbPref3 = gtk.HBox()

        self.labelGUIs = gtk.Label(self.text['pref_gui'])
        self.labelGUIs.set_justify(gtk.JUSTIFY_LEFT)

        for (index, item) in enumerate(self.libguis['index']):
            if self.libgui == item:
                self.comboLibGui.set_active(index)

        self.hbPref1.pack_start(self.labelGUIs, False, False, 0)
        self.hbPref1.pack_start(self.comboLibGui, False, False, 1)

        self.labelText = gtk.Label(self.text['pref_reload'])

        self.labelOut = gtk.Label(self.text['pref_out'])
        self.labelOut.set_justify(gtk.JUSTIFY_LEFT)

        for (index, item) in enumerate(self.outs['index']):
            if self.out == item:
                self.comboOuts.set_active(index)

        self.hbPref2.pack_start(self.labelOut, False, False, 0)
        self.hbPref2.pack_start(self.comboOuts, False, False, 1)

        self.labelDir = gtk.Label(self.text['pref_dir'])
        self.labelDir.set_justify(gtk.JUSTIFY_LEFT)

        for (index, item) in enumerate(self.fileChooser['dir']['index']):
            if self.current_folder == item:
                self.comboCurrentDir.set_active(index)

        self.hbPref3.pack_start(self.labelDir, False, False, 0)
        self.hbPref3.pack_start(self.comboCurrentDir, False, False, 1)

        self.dialog.vbox.pack_start(self.hbPref1, False, False, 0)
        self.dialog.vbox.pack_start(self.labelText, False, False, 1)
        self.dialog.vbox.pack_start(self.hbPref2, False, False, 2)
        self.dialog.vbox.pack_start(self.hbPref3, False, False, 3)

    def create_view_precalcul(self):
        self.dialog.set_title(self.title['mainWindow'])
        self.store = gtk.ListStore(str, str, str)

        self.view = gtk.TreeView()
        self.view.set_model(self.store)

        self.cellFile = gtk.CellRendererText()
        self.colFile = gtk.TreeViewColumn(self.title['col_file'], self.cellFile,
            text=0, foreground=1, background=2)

        bg = 'white'
        fg = 'black'

        for k, v in self.files['base'].items():
            self.store.append([v, fg, bg])

        self.view.append_column(self.colFile)

        self.window = gtk.ScrolledWindow()
        self.window.add_with_viewport(self.view)

        self.dialog.vbox.pack_start(self.window, True, True, 0)


    def create_view_table(self):

        self.dialog.set_title(self.title['mainWindow'] + ' - ' +
                              self.title['window_dialog_result'])
        self.store = gtk.ListStore(str, str, str, str, str, str)

        self.view = gtk.TreeView()
        self.view.set_model(self.store)

        self.cellFile = gtk.CellRendererText()
        self.cellSum = gtk.CellRendererText()
        self.cellSize = gtk.CellRendererText()
        self.cellDate = gtk.CellRendererText()

        #self.cellSize.set_property('alignment', pango.ALIGN_RIGHT) # avalaible in 2.10!?
        self.cellSize.set_property('xalign', 1.0)

        self.colFile = gtk.TreeViewColumn(self.title['col_file'], self.cellFile,
            text=0, foreground=4, background=5)
        self.colSum = gtk.TreeViewColumn(self.title['col_checksum'], self.cellSum,
            text=1, foreground=4, background=5)
        self.colSize = gtk.TreeViewColumn(self.title['col_size'], self.cellSize,
            text=2, foreground=4, background=5)
        self.colDate = gtk.TreeViewColumn(self.title['col_date'], self.cellDate,
            text=3, foreground=4, background=5)

        self.store_append()

        self.view.append_column(self.colFile)
        self.view.append_column(self.colSum)
        self.view.append_column(self.colSize)
        self.view.append_column(self.colDate)

        self.window = gtk.ScrolledWindow()
        self.window.add_with_viewport(self.view)

        self.dialog.vbox.pack_start(self.window, True, True, 0)

        if self.action == 'calcul' or self.action == 'calculFolder':
            labelSave = gtk.Label(self.text['checksum_save'])
            self.dialog.vbox.pack_start(labelSave, True, True, 1)

    def precalcul_yes(self, button):
        self.result = True
        self.dialog.destroy()

    def precalcul_no(self, button):
        self.result = False
        self.dialog.destroy()

    def run(self):

        self.init_vars()

        self.log.info('=> Displaying Window Dialog')

        self.dialog = gtk.Dialog()
        self.dialog.set_resizable(False)
        self.dialog.set_size_request(400, 300)

        if self.action == 'pref':
            self.dialog.set_property('icon-name','gtk-preferences')
            self.current_folder_filechooser()
            self.out_system()
            self.create_view_pref()
        elif self.action == 'precalcul':
            self.dialog.set_property('icon-name','dialog-information')
            self.create_view_precalcul()
        else:
            self.dialog.set_property('icon-name','dialog-information')
            self.create_view_table()

        self.create_buttons()

        self.dialog.show_all()
        self.dialog.run()
        self.dialog.destroy()

        self.log.info('=> Destroying Window Dialog')

    def current_folder_filechooser(self):
        ''' Define variable current_dir... '''

        setattr(self, 'current_folder',
            file(os.path.join(self.dir, self.dirs[0], 'current_folder')).read() )
        if self.current_folder not in self.fileChooser['dir']['index']:
            self.current_folder = 'current'

    def destroy(self, button):
        self.dialog.destroy()

    def saver(self, button):

        array = {
            'algo': self.algo,
            'algos': self.algos,
            'action': gtk.FILE_CHOOSER_ACTION_SAVE,
            'dir': self.dir,
            'dirs': self.dirs,
            'generator': self.generator,
            'fileChooser': self.fileChooser,
            'files': self.files,
            'filters': self.filters,
            'outs': self.outs,
            'select_multiple': False,
            'text': self.text,
            'title': self.title['window_saving'],
            'version': self.version,
        }

        WFC = Window_FileChooser(array)
        WFC.set_debug(self.debug)
        WFC.set_log(self.log)
        WFC.run()

        self.dialog.destroy()

    def set_debug(self, entry):
        self.debug = bool( entry )

    def set_log(self, entry):
        self.log = entry

    def store_append(self):

        bg = 'white'
        fg = 'black'

        if self.action == 'calcul':
            array = self.files['base']

        elif self.action == 'calculFolder':
            array = self.files['shortpath']

        elif self.action == 'controlByFile':
            array = self.files['name']

        for k, v in array.items():
            name = v
            checksum = self.files['checksum'][k]

            if 'date' in self.files and self.files['date'] is not None:
                date = self.files['date'][k]
            else:
                date = ''

            if 'size' in self.files and self.files['size'] is not None:
                size = self.files['size'][k]
            else:
                size = ''

            if 'result' in self.files:
                if self.files['result'][k]:
                    bg = 'green'
                else:
                    bg = 'red'

            self.store.append([name, checksum, size, date, fg, bg])

        del(array)

        self.log.debug('WD: Generate cell\'s store: %(name)s and %(checksum)s '
            % {'checksum': self.files['checksum'][k], 'name': v })

    def write_file(self):
        for key, value in self.pref.items():
            f = file(os.path.join(self.dir, self.dirs[0], key), 'w')
            f.write(value)
            f.close()

        self.labelText.set_text(self.text['pref_saved'])
