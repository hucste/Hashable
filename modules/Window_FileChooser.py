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
    from modules import XML_Parser
    XML_Parser = XML_Parser.XML_Parser
    #error = False
except:
    print 'Cant import module XML_Parser onto Window_FileChooser'
    #error = True
    sys.exit(1)

class Window_FileChooser:
    'Display a Dialog File Chooser'

    def __init__(self, array):
        self.dic = array

    def current_folder_filechooser(self):
        ''' Define variable current_dir... '''

        setattr(self, 'current_folder',
            file(os.path.join(self.dir, self.dirs[0], 'current_folder')).read() )
        if self.current_folder not in self.fileChooser['dir']['index']:
            self.current_folder = 'current'

    def get_fileChoosed(self):
        ''' Get file choosed '''

        if hasattr(self, 'fileChoosed'):
            return self.fileChoosed
        else:
            return False

    def get_filesChoosed(self):
        ''' Get files choosed '''

        if hasattr(self, 'filesChoosed'):
            return self.filesChoosed
        else:
            return False

    def init_vars(self):
        ''' Initialize variables needed '''

        for d in self.dic:
            setattr(self, d, self.dic[d])

            self.log.debug('Window FileChooser: Create variable self.%s needed...'
                % d)

    def out_system(self):
        ''' Define variable out... for output file '''

        setattr(self, 'out',
            file(os.path.join(self.dir, self.dirs[0], 'out')).read() )
        if self.out not in self.outs['index']:
            self.out = 'xml'

    def run(self):
        ''' Launcher methodes '''

        self.init_vars()

        self.log.info('WFC => Displaying Window FileChooser')
        self.current_folder_filechooser()
        self.out_system()

        chooser = gtk.FileChooserDialog(
            title=self.title,
            action=self.action,
            buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,
                gtk.RESPONSE_OK))

        chooser.set_current_folder(self.current_folder)

        if self.action == gtk.FILE_CHOOSER_ACTION_SAVE:

            if hasattr(self, 'algo'):
                if 'base' in self.files['folder']:
                    self.current = self.files['folder']['base'] + '.'  + self.algo
                else:
                    self.current = self.files['base'][0] + '.' + self.algo
            else:
                self.current = self.files['base'][0]

            if self.out == 'xml':
                self.current = self.current + '.xml'

            #chooser.set_action(gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER)
            chooser.set_current_name(self.current)
            chooser.set_do_overwrite_confirmation(True)

        chooser.set_property('icon-name','folder')
        chooser.set_select_multiple(self.select_multiple)

        if self.filters <> '*':
            ff = gtk.FileFilter()
            ff.set_name(self.text['filter_name'])

            #if self.out == 'txt':
                #ff.add_mime_type('text/plain')
            for (index, item) in enumerate(self.filters['index']):
                ff.add_pattern('*.%s' % item)

                self.log.debug('WFC => add filter %s' % item)

            #elif self.out == 'xml':
                #ff.add_mime_type('application/xml')
            ff.add_pattern('*.xml')

            chooser.add_filter(ff)

        response = chooser.run()

        if response == gtk.RESPONSE_OK:

            if self.action == gtk.FILE_CHOOSER_ACTION_OPEN:
                if self.select_multiple:
                    self.filesChoosed = chooser.get_filenames()

                else:
                    self.fileChoosed = chooser.get_filename()

            elif self.action == gtk.FILE_CHOOSER_ACTION_SAVE:
                self.save_file(chooser.get_filename())

            elif self.action == gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER:
                self.fileChoosed = chooser.get_filename()

        chooser.destroy()
        self.log.info('WFC => Destroying Window FileChooser')

    def save_file(self, filename):
        ''' Save informations on file system '''

        try:
            if self.out == 'txt':
                f = open(filename, 'w')
                print self.files

                if 'shortpath' in self.files and self.files['shortpath']:
                    for key, value in self.files['shortpath'].items():
                        f.write(self.files['checksum'][key] + ' ' + value + '\n')

                elif 'base' in self.files and self.files['base']:
                    for key, value in self.files['base'].items():
                        f.write(self.files['checksum'][key] + ' ' + value + '\n')

                f.close()

            elif self.out == 'xml':
                array = {
                    'algorithm': self.algo,
                    'generator': self.generator,
                    'files': self.files,
                    'id': os.path.basename(filename),
                    'version': self.version,
                }

                parser = XML_Parser()
                parser.set_debug(self.debug)
                parser.set_dict(array)
                parser.set_log(self.log)
                parser.build_xml()
                parser.save_xml(filename)

        except IOError as ioe:
            self.log.exception('Error to create document: %s' % ioe)
            return False

    def set_debug(self, entry):
		self.debug = bool( entry )

	def set_log(self, entry):
		self.log = entry
