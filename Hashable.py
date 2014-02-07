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

''' Hashable Calculator is a software to calculate or control checksum '''

#
# *** DONT TOUCH BELOWE!
#

# modules needed
import gettext
import logging, logging.config, logging.handlers
import os
import sys

#
## GLOBAL DEFINITION
#
## i18n (internationalisation)
gettext.bindtextdomain('Hashable', 'locale')
gettext.textdomain('Hashable')
#gettext.install('Hashable')
_ = gettext.gettext

NAME = 'Hashable Calculator'

class Hashable:
    '''Application Hashable Calculator'''

    def __init__(self):
        self.init_arrays()
        self.init_vars()

        self.log_me()
        self.log.info('*** Launching Hashable Calculator ***')
        self.log.debug('actions: %s \n authors: %s \n text: %s \n title: %s' %
            (self.actions, self.authors, self.text, self.title))

    def auto_loader(self):
        '''Autoload my modules'''

        try:

            [sys.path.append(os.path.join(self.dir, d)) for d in self.dirs]

            import modules

            self.log.info('Attempt to autoload my modules ...')
            self.log.debug(modules.__all__)

            for module in modules.__all__:
                globals()[module] = getattr(__import__('modules', globals(),
                    locals(), [module], -1), module)

                self.log.debug('Import modules ' + str(module))

        except ImportError as ie:
            mssg = 'Cant import modules Window_Hashable onto script Hashable. \
                    Error: '
            self.log.exception( mssg + ie)
            sys.exit(1)

    def log_me(self):
        ''' Logger '''
        logging.config.fileConfig(
            os.path.join(self.dir, self.dirs[0], 'log.conf'))
        self.log = logging.getLogger('root')

        if not self.debug:
            self.log.setLevel(logging.INFO)
        else:
            self.log.setLevel(logging.DEBUG)

    def init_arrays(self):
        ''' Initialize all dict, list needed '''

        self.actions = {
            'index': ['calcul', 'calculFolder', 'control', 'controlByFile'],
            'calcul': { 'active': True,
                        'label': _(u'Calculate'), },
            'calculFolder': { 'active': True,
                              'label': _(u'Calculate a folder'), },
            'control': { 'active': True,
                         'label': _(u'Control'), },
            'controlByFile': { 'active': True,
                               'label': _(u'Control by file'), },
        }

        self.authors = [ u'Stéphane HUC']

        self.dirs = ['conf', 'glades', 'license', 'locale', 'log', 'modules']

        self.files = {
            'conf': ['debug', 'GUI.conf', 'log.conf', 'out'],
        }

        self.fileChooser = dict()
        self.fileChooser['dir'] = {
            'index': ['current', 'home'],
            'current': { 'active': True, 'label': _(u'Current folder') },
            'home': { 'active': True, 'label': _(u'Home directory') }, # os.path.expanduser("~")
        }

        self.icons = {
            'about': '/usr/share/icons/gnome/16x16/actions/help-about.png',
            'error': '/usr/share/icons/gnome/16x16/status/gtk-dialog-error.png',
            'info': '/usr/share/icons/gnome/16x16/status/gtk-dialog-info.png',
            'question': '/usr/share/icons/gnome/16x16/status/gtk-dialog-question.png',
            'warning': '/usr/share/icons/gnome/16x16/status/gtk-dialog-warning.png',
        }

        self.labels = {
            'calcul': _(u'Choose one or more files:'),
            'calculFolder': _(u'Choose one folder:'),
            'control': _(u'Choose a file to act:'),
            'controlByFile': _(u'Choose your checksum file:'),
        }

        self.libguis = {
            'index': ['gtkbuilder', 'libglade', 'webkit'],
            'gtkbuilder': { 'active': True,
                            'label': 'GtkBuilder' },
            'libglade': { 'active': True,
                          'label': 'Glade' },
            'webkit': { 'active': False,
                        'label': 'Webkit' },
        }

        self.mimes = {
            'txt': 'text/plain',
            'xml': 'application/xml',
        }

        self.outs = {
            'index': ['txt', 'xml'],
            'txt': { 'active': True, 'label': _(u'Text') },
            'xml': { 'active': True, 'label': _(u'XML') },
        }

        self.text = {

            'about_comments':
                _(u'Software to calcul or control checksum file...'),

            'btnApply': _(u'Apply'),
            'btnCancel': _(u'Cancel'),
            'btnNo': _(u'No'),
            'btnOk': _(u'OK'),
            'btnQuit': _(u'Quit'),
            'btnYes': _(u'Yes'),

            'checksum_bad':
                _(u'Error: Your checksum is bad! \nYour archive seems corrupt. :('),
            'checksum_good':
                _(u'Yeahhh: \nGood checksum egual good archive! \n :D'),
            'checksum_mssg':
                _(u'For the file %(file)s, your checksum is \n %(checksum)s \n'),
            'checksum_save':
                _(u'Do you want to save checksums in file?'),
            'checksum_warn_empty':
                _(u'Your checksum is empty, please fill-it!'),

            'diff_algo':
                _(u'The algorithm choosed (%(algo)s) and algorithm in checksum file ') +
                _(u'(%(algorithm)s) are different!\nAre you sure of your choise?'),
            'diff_file':
                _(u'The file choosed (%(fileName)s) and file in checksum file ') +
                _(u'(%(checksumFile)s) are different!\n Are you sure?'),
            'diff_generator':
                _(u'The value generator, in xml file, seems different: %s'),

            'error_algo_xml':
                _(u'Error: The algorithm specified %(algorithm)s in checksum file ') +
                _(u'is not supported!'),
            'error_hash':
                _(u'Error: It seems to be an error during creation of the hash!'),
            'error_key_hash':
                _(u'Error: The key %s in dict hashlib not exists... Booo!'),
            'error_version':
                _(u'Your python\'s version is too oldier. (version: %s)\n') +
                _(u'Please upgrade, at minimum, to 2.5!'),

            'filter_name': _(u'All Files'),

            'itemAbout': _(u'About'),
            'itemEdit': _(u'Edit'),
            'itemFile': _(u'_Files'),
            'itemHelp': _(u'H_elp'),
            'itemNew': _(u'_New'),
            'itemPref': _(u'Preferences'),
            'itemQuit': _(u'Quit'),

            'labelAction': _(u'Choose an action:'),
            'labelDirs': _(u'Choose one folder:'),
            'labelFile': _(u'Choose a file to act:'),
            'labelFiles': _(u'Choose one or more files:'),
            'labelHash': _(u'Choose an algorithm:'),
            'labelOutFile': _(u'Choose your file out:'),
            'labelSum': _(u'Copy your checksum, here:'),
            'labelSumFile': _(u'Choose your checksum file:'),

            'option_r': _(u'recursive:'),

            'pref_dir': _(u'Folder preferred for File Chooser:'),
            'pref_gui': _(u'GUI Project:'),
            'pref_out': _(u'Choose your file out:'),
            'pref_reload': _(u'Need to restart the program to apply the new preferences!'),
            'pref_saved': _(u'The preferences are saved. \nClose this window and restart the program!'),

            'progress_end': _(u'Process ending!'),
            'progress_init': _(u'Initialize...'),
            'progress_run': _(u'Processing...'),
            'progress_wait': _(u'Wait...'),

            }

        self.title = {

            'col_checksum': _(u'Checksum'),
            'col_date': _(u'Date'),
            'col_file': _(u'File'),
            'col_size': _(u'Size'),

            'error_version': _(u'Python Error Version'),

            'mainWindow': _(NAME),

            'window_dialog_pref': _(u'Preferences'),
            'window_dialog_result': _(u'Files and Checksums results!'),
            'window_saving': _(u'Saving yours checksums!'),

            }

    def init_vars(self):
        ''' Initialize variables needed '''
        setattr(self, 'dir', os.getcwd())

        setattr(self, 'debug',
            file(os.path.join(self.dir, self.dirs[0], 'debug')).read())
        if self.debug != '0':
            self.debug = True
        else:
            self.debug = False

        setattr(self, 'license',
            file(os.path.join(self.dir, self.dirs[2], 'gpl3.txt')).read())

        setattr(self, 'libgui',
            file(os.path.join(self.dir, self.dirs[0], 'gui')).read())
        if self.libgui not in self.libguis['index'] :
            self.libgui = 'libglade'

        setattr(self, 'version',
            file(os.path.join(self.dir, 'VERSION')).read())

    def rebuild_dict(self, array):
        for a in array['index']:
            if not array[a]['active']:
                array['index'].remove(a)

        return array

    def run(self):
        ''' Launcher main '''
        self.actions = self.rebuild_dict(self.actions)
        self.libguis = self.rebuild_dict(self.libguis)
        self.outs = self.rebuild_dict(self.outs)

        init = dict()
        init = {
            'actions': self.actions,
            'authors': self.authors,
            'debug': self.debug,
            'dir': self.dir,
            'dirs': self.dirs,
            'fileChooser': self.fileChooser,
            'generator': NAME,
            'icons': self.icons,
            'labels': self.labels,
            'libgui': self.libgui,
            'libguis': self.libguis,
            'license': self.license,
            'log': self.log,
            'mimes': self.mimes,
            #'out': self.out,
            'outs': self.outs,
            'text': self.text,
            'title': self.title,
            'version': self.version,
        }

        if self.libgui == 'webkit':
            wgl = Window_Webkit.Window_Webkit(init)

        else:
            wgl = Window_Glade.Window_Glade(init)

        wgl.run()
        wgl.main()

if __name__ == '__main__':

    APP = Hashable()
    APP.auto_loader()
    APP.run()
