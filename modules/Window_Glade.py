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
import gettext
import gobject
import glob
import hashlib
import mimetypes
import os
import platform
import sys
import time
import thread, threading

try:
    import pygtk
    pygtk.require('2.0')
except:
    print 'Cant import pygtk'

try:
    import gtk
    import gtk.glade
except:
    print 'Cant import gtk'
    sys.exit(1)
#
from time import sleep

try:
    from modules import Window_About
    from modules import Window_Dialog
    from modules import Window_FileChooser
    from modules import Window_Message
    from modules import XML_Parser
    #
    Window_About = Window_About.Window_About
    Window_Dialog = Window_Dialog.Window_Dialog
    Window_Message = Window_Message.Window_Message
    Window_FileChooser = Window_FileChooser.Window_FileChooser
    XML_Parser = XML_Parser.XML_Parser
except:
    print 'Cant import modules Window_* onto Window_Hashable'
    sys.exit(1)

#
## GLOBAL DEFINITION
#

## initialisation du thread
gtk.gdk.threads_init()
##

#
## CLASSES
#
class Window_Glade:
    '''Building GUI Glade'''

    def __getattr__(self, key):

        if self.libgui == 'gtkbuilder':
            return self.gui.get_object(key)
        elif self.libgui == 'libglade':
            return self.gui.get_widget(key)

    def __getitem__(self, key):
        if self.libgui == 'gtkbuilder':
            return self.gui.get_object(key)
        elif self.libgui == 'libglade':
            return self.gui.get_widget(key)

    def __init__(self, init):

        for i in init:
            setattr(self, i, init[i])

        self.log.info('=> Displaying Window Glade')

        self.init_vars()
        self.init_arrays()

        mimetypes.init()

    def add_filters(self):
        ''' Create filters to include on FileChooser '''
        # generer c bien, mais comment les afficher ???
        ff = gtk.FileFilter()
        ff.set_name(self.text['filter_name'])

        for m in self.mimes:
            ff.add_mime_type(m)

        ff.add_pattern('*.xml')

        for a in self.algos:
            ff.add_pattern('*.%s' % a)

            self.log.debug('WG => add filter %s' % a)

        self.btnSumFilter.set_filter(ff)

    def auto_connect_events(self):
        ''' Auto-connector events '''
        events = {}

        for (key, value) in self.__class__.__dict__.items():
            if callable(value) and key.startswith('on_'):
                events[key[3:]] = getattr(self, key)

        if self.libgui == 'gtkbuilder':
            self.gui.connect_signals(events)
        elif self.libgui == 'libglade':
            self.gui.signal_autoconnect(events)

    def build_infos_files(self):
        ''' Build dict files by files information '''

        if 'name' in self.files:
            for k, v in self.files['name'].items():
                self.files['base'][k] = os.path.basename(v)
                #self.files['size'][k] = os.path.getsize(v)
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(v)
                self.files['size'][k] = size
                self.files['timestamp'][k] = mtime
                self.files['date'][k] = time.ctime(mtime)

    def build_infos_files_by_file(self):
        ''' Create dict files by informations on file control '''

        if hasattr(self, 'txt') and self.txt is not None:
            array = self.txt

        elif hasattr(self, 'xml') and self.xml is not None:
            array = self.xml

        if 'name' in array:
            for k, v in array['name'].items():
                self.files['name'][k] = os.path.join(self.file['dir'], v)

        del(array)

    def build_mssg_calcul(self):
        ''' Build message for calcul action '''
        self.end = True
        self.flag = ''

        array = {
            'algo': self.algo,
            'algos': self.algos,
            'action': self.action,
            'actions': self.actions,
            'dir': self.dir,
            'dirs': self.dirs,
            'generator': self.generator,
            'fileChooser': self.fileChooser,
            'files': self.files,
            'filters': self.algos,
            'outs': self.outs,
            'text': self.text,
            'title': self.title,
            'version': self.version,
        }

        WD = Window_Dialog(array)
        WD.set_debug(self.debug)
        WD.set_log(self.log)
        WD.run()

    def build_mssg_calculFolder(self):
        ''' Build message for calculFolder '''

        print self.files

        sys.exit()

    def build_mssg_control(self):
        ''' Build message for control action '''

        if cmp(self.checksum, self.files['checksum'][0]) == 0:
            self.end = True
            self.flag = 'info'
            self.mssg = self.text['checksum_good']

        else:
            self.flag = 'error'
            self.mssg = self.text['checksum_bad']

    def build_mssg_controlByFile(self):
        ''' Build message for action 'control by file' '''

        if hasattr(self, 'txt') and self.txt is not None:
            self.control_by_file_txt()

        elif hasattr(self, 'xml') and self.xml is not None:
            self.control_by_file_xml()

        array = {
            'algo': self.algo,
            'algos': self.algos,
            'action': self.action,
            'actions': self.actions,
            #'checksum': self.checksum,
            'dir': self.dir,
            'dirs': self.dirs,
            #'file': os.path.basename(self.file),
            'files': self.result,
            'filters': self.algos,
            'outs': self.outs,
            'text': self.text,
            'title': self.title,
            'version': self.version,
        }

        WD = Window_Dialog(array)
        WD.set_debug(self.debug)
        WD.set_log(self.log)
        WD.run()

        self.end = True
        self.flag = ''
        self.mssg = ''

    def calcul_checksums(self):
        ''' Calcul all checksums needed '''

        for k, v in self.files['hash'].items():
            if os.path.exists(self.files['name'][k]):
                try:

                    f = open(self.files['name'][k], 'rb')
                    lines = f.readlines()
                    f.close()

                except IOError as ioe:
                    self.log.exception('We have a problem to open file %(file)s; \
                        Error is: %(ioe)s' %
                        {'file': self.files['name'][k], 'ioe': ioe})
                    self.exit()

                if lines:
                    x = 0
                    for l in lines:
                        self.files['hash'][k].update(l)
                        x += 1

                self.files['checksum'][k] = self.files['hash'][k].hexdigest()
            else:
                self.files['checksum'][k] = 0

        if self.files['checksum'] is not None:
            return True
        else:
            return False

    def chooser_checksumFile(self):
        ''' Get Checksum File '''

        self.fileChecksum = self.WFC.get_fileChoosed()

    def chooser_files(self):
        ''' Get Files choosed '''

        self.files['name'] = dict(enumerate(self.WFC.get_filesChoosed()))

        self.build_infos_files()

        if self.action == 'calcul':
            self.display_precalc_window()

    def chooser_folder(self):
        ''' Get Folder choosed to calculate checksum '''

        self.folder = dict()

        self.folder['choosed'] = self.WFC.get_fileChoosed()
        self.folder['list'] = self.list_directory(self.folder['choosed'])

        self.files['folder']['base'] = os.path.basename(self.folder['choosed'])
        self.files['folder']['dirname'] = os.path.dirname(self.folder['choosed'])
        self.files['folder']['name'] = self.folder['choosed']

        for k, v in enumerate(self.folder['list']):
            self.files['name'][k] = v
            s = v.split(self.files['folder']['name'])
            self.files['shortpath'][k] = s[1][1:]
            del(s)

        self.build_infos_files()

    def control_by_file_txt(self):
        ''' Build variable txt result if checksums are sames '''

        self.txt['result'] = dict()

        for k, v in self.txt['checksum'].items():
            if cmp(v, self.files['checksum'][k]) == 0:
                self.txt['result'][k] = True

            else:
                self.txt['result'][k] = False

        self.result = self.txt

    def control_by_file_xml(self):
        ''' Control variable xml and
        Build variable xml result if checksums are sames '''

        if self.xml['generator'] <> self.generator:
            self.flag = 'warning'
            self.mssg = self.text['diff_generator'] % self.xml['generator']

        elif self.algo <> self.xml['algorithm']:
            self.flag = 'warning'
            self.mssg = self.text['diff_algo'] % {'algo': self.algo,
                'algorithm': self.xml['algorithm']}
        else:
            self.xml['result'] = dict()

            for k, v in self.xml['checksum'].items():
                if cmp(v, self.files['checksum'][k]) == 0:
                    self.xml['result'][k] = True

                else:
                    self.xml['result'][k] = False

            self.result = self.xml

    def create_gui(self):
        ''' Create UI '''

        if self.libgui == 'gtkbuilder':
            self.gui = gtk.Builder()
            self.gui.add_from_file ('glades/Hashable.gtkbuilder.glade')

        elif self.libgui == 'libglade':
            self.gladeFile = 'glades/Hashable.libglade.glade'
            self.gui = gtk.glade.XML(self.gladeFile, 'mainWindow')

    def create_hash(self):
        ''' Create Hash '''

        # if checksum file, necessary to buil self.files, before hashes
        if self.action == 'controlByFile':
            self.get_infosByFile()

        # creating hashes
        if 'name' in self.files:
            if 0 not in self.files['name']:
                self.build_infos_files()

            for k, v in self.files['name'].items():
                self.files['hash'][k] = hashlib.new(self.algo)

                self.log.debug('WG: Create hash %(hash)s for file %(file)s' % {
                    'file': self.files['name'][k],
                    'hash': self.files['hash'][k]})

            return True

        else:
            self.flag = 'error'
            self.mssg = self.text['error_hash']

            return False

    def create_status_icon(self):
        ''' Create Status Icon '''
        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.connect('activate', self.on_click_statusIcon)
        self.statusIcon.connect('popup-menu', self.on_menu_statusIcon)
        self.statusIcon.set_from_icon_name('accessories-calculator')
        self.statusIcon.set_tooltip(self.title['mainWindow'])
        self.statusIcon.set_visible(True)

    def create_window(self):
        ''' Create main window '''
        self.mainWindow.connect('delete_event', gtk.main_quit)
        self.mainWindow.connect('destroy', self.destroy_app)
        self.mainWindow.set_property('icon-name','accessories-calculator')
        self.mainWindow.set_opacity(0.95)
        self.mainWindow.set_resizable(False)
        self.mainWindow.set_size_request(400, 300)
        self.mainWindow.set_title(self.title['mainWindow'])

        # add accelerator group
        self.ag = gtk.AccelGroup()
        self.mainWindow.add_accel_group(self.ag)

    def destroy_app(self):
        ''' Quit software '''
        gtk.timeout_remove(self.tempo)
        self.tempo = 0
        gtk.main_quit()

    def display_about_window(self):
        ''' Display about dialog '''

        array = {
            'authors': self.authors,
            'comments': self.text['about_comments'],
            'copyright': self.authors[0] + u' © ' + self.year,
            'icon': self.icons['about'],
            'license': self.license,
            'name': self.title['mainWindow'],
            'program_name': self.title['mainWindow'],
            'version': self.version,
            'website': self.website,
        }

        WA = Window_About(array)
        WA.set_debug(self.debug)
        WA.set_log(self.log)
        WA.run()

    def display_mssg_window(self):
        ''' Display message window '''

        array = {
            'algo': self.algo,
            'algos': self.algos,
            'checksum': self.sumHash,
            'gtkbtn': self.gtkBtnOk,
            'file': self.fileName,
            'fileChooser': self.fileChooser,
            'flag': self.flag,
            'mssg': self.mssg,
            'version': self.version,
        }

        WM = Window_Message(array)
        WM.set_debug(self.debug)
        WM.set_log(self.log)
        WM.run()

    def display_precalc_window(self):
        array = {
            'algo': self.algo,
            'algos': self.algos,
            'action': 'precalcul',
            'actions': self.actions,
            'dir': self.dir,
            'dirs': self.dirs,
            'files': self.files,
            'filters': self.algos,
            'outs': self.outs,
            'text': self.text,
            'title': self.title,
            'version': self.version,
        }

        WD = Window_Dialog(array)
        WD.set_debug(self.debug)
        WD.set_log(self.log)
        WD.run()

        if not WD.get_result():
            self.init_arrays()
            self.on_btnFile_clicked(self.btnFile)
        else:
            self.execute_hash()

    def display_pref_window(self):
        ''' Display window preferences '''
        self.comboCurrentDir = gtk.ComboBox()
        self.comboCurrentDir = self.fill_combo(self.comboCurrentDir, self.fileChooser['dir'])

        self.comboLibGui = gtk.ComboBox()
        self.comboLibGui = self.fill_combo(self.comboLibGui, self.libguis)

        self.comboOuts = gtk.ComboBox()
        self.comboOuts = self.fill_combo(self.comboOuts, self.outs)

        array = {
            'action': 'pref',
            'actions': self.actions,
            'comboCurrentDir': self.comboCurrentDir,
            'comboLibGui': self.comboLibGui,
            'comboOuts': self.comboOuts,
            'dir': self.dir,
            'dirs': self.dirs,
            'fileChooser': self.fileChooser,
            'generator': self.generator,
            'libgui':    self.libgui,
            'libguis': self.libguis,
            'outs':    self.outs,
            'text': self.text,
            'title': self.title,
            'version': self.version,
        }

        WD = Window_Dialog(array)
        WD.set_debug(self.debug)
        WD.set_log(self.log)
        WD.run()

    def execute_hash(self):
        ''' all operations to making checksums '''

        self.end = False

        self.progressBar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
        self.manage_progressBar()

        if self.verify_txtSum_empty():

            self.gtkBtnOk = gtk.BUTTONS_OK

            if self.create_hash():

                if self.calcul_checksums():

                    if self.action == 'calcul':
                        self.build_mssg_calcul()

                    elif self.action == 'calculFolder':
                        self.build_mssg_calcul()

                    elif self.action == 'control':
                        self.build_mssg_control()

                    elif self.action == 'controlByFile':
                        self.build_mssg_controlByFile()

        if self.flag <> '':
            self.display_mssg_window()

        if self.end:
            self.re_init_all()

    def exit(self):
        ''' Bye-bye software '''
        print 'You have a seriously error in the class Window Glade...\n \
                Please see file log !'
        sys.exit(1)

    def file_chooser(self):
        ''' When files are choosed '''

        # build necessary dict
        if self.action == 'calculFolder':
            array = {
                'action': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                'dir': self.dir,
                'dirs': self.dirs,
                'fileChooser': self.fileChooser,
                'filters': '*',
                'outs': self.outs,
                'select_multiple': True,
                'text': self.text,
                'title': self.title['mainWindow'] + ' - ' +
                         self.text['labelFiles'],
            }

        elif self.action == 'controlByFile':
            array = {
                'action': gtk.FILE_CHOOSER_ACTION_OPEN,
                'dir': self.dir,
                'dirs': self.dirs,
                'fileChooser': self.fileChooser,
                'files': self.files,
                'filters': self.algos,
                'outs': self.outs,
                'select_multiple': False,
                'text': self.text,
                'title': self.title['mainWindow'] + ' - ' +
                         self.text['labelSumFile'],
            }

        else:
            array = {
                'action': gtk.FILE_CHOOSER_ACTION_OPEN,
                'dir': self.dir,
                'dirs': self.dirs,
                'fileChooser': self.fileChooser,
                'filters': '*',
                'outs': self.outs,
                'select_multiple': True,
                'text': self.text,
                'title': self.title['mainWindow'] + ' - ' +
                         self.text['labelFiles'],
            }

        # appel
        self.WFC = Window_FileChooser(array)
        self.WFC.set_debug(self.debug)
        self.WFC.set_log(self.log)
        self.WFC.run()

        # on recupere le(s) fichier(s) choisi(s)
        if self.action == 'calculFolder':
            self.chooser_folder()

        elif self.action == 'controlByFile':
            self.chooser_checksumFile()

        else:
            self.chooser_files()

        # set sensitives !
        if self.action <> 'control':
            self.btnGo.set_sensitive(True)

    def fill_combo(self, widget, array):
        ''' Fill combobox '''
        store = gtk.ListStore(str)

        for k, v in enumerate(array['index']):
            if array[v]['active']:
                item = array[v]['label']
                store.append([item])

        #widget.set_active(0)
        widget.set_model(store)

        if type(widget) == gtk.ComboBoxEntry:
            widget.set_text_column(0)

        elif type(widget) == gtk.ComboBox:
            cell = gtk.CellRendererText()
            widget.pack_start(cell, True)
            widget.add_attribute(cell, 'text', 0)

        return widget

    def get_algorithms(self):
        ''' Get algorithms supported by hashlib '''

        self.algos = dict()
        self.algos['index'] = hashlib.algorithms

        for (index, item) in enumerate(self.algos['index']):
            self.algos[item] = dict()
            self.algos[item]['active'] = True
            self.algos[item]['label'] = item.upper()

    def get_infosByFile(self):
        ''' Get informations needed for the control by file '''

        self.file = dict()
        self.file['dir'] = os.path.dirname(self.fileChecksum)
        self.file['shortname'], self.file['ext'] = os.path.splitext(self.fileChecksum)
        self.file['ext'] = self.file['ext'][1:]
        self.file['type'], self.file['encoding'] = mimetypes.guess_type(self.fileChecksum)

        self.log.debug('WG => get infos by file checksum: %s' % self.file)

        # segun output choosed... read good file! :p
        if self.file['type'] == self.mimes['xml']:
            self.read_file_xml()

            self.verify_algo_xml()

        else:
            self.read_file_txt()

        self.build_infos_files_by_file()

    def init_arrays(self):
        ''' Initialize dicts files '''

        infos = ['base', 'checksum', 'date', 'folder', 'hash', 'name',
            'shortpath', 'size', 'timestamp']

        for i in infos:
            self.files[i] = dict()


    def init_thread(self):
        ''' Initialize thread ''' # not use for the moment!
        t = thread.start_new_thread(self.up_progressBar, ())

    def init_vars(self):
        ''' Initialize variables needed '''
        self.action = ''
        self.algo = ''
        self.files = dict()
        self.pyVersion = platform.python_version()
        self.year = time.strftime('%Y', time.localtime())
        self.website = 'http://dev.stephane-huc.net/HashableCalculator/'

    def list_directory(self, path):
        ''' get file arborescence in list '''

        l = list()
        files = glob.iglob(os.path.join(path, '*'))

        for f in files:
            if os.path.isdir(f):
                if self.option_r:
                    l.extend(self.list_directory(f))
            else:
                l.append(f)

        return l

    def main(self):
        ''' Main software '''
        gtk.main()

    def manage_menu(self):
        ''' Manage menubar '''
        # manage menu
        self.itemAbout.set_label(self.text['itemAbout'])
        self.itemEdit.set_label(self.text['itemEdit'])
        self.itemFile.set_label(self.text['itemFile'])
        self.itemHelp.set_label(self.text['itemHelp'])
        self.itemNew.set_label(self.text['itemNew'])
        self.itemPref.set_label(self.text['itemPref'])
        self.itemQuit.set_label(self.text['itemQuit'])

        # add accelerators
        self.itemPref.add_accelerator('activate', self.ag, gtk.keysyms.P,
            gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        self.itemQuit.add_accelerator('activate', self.ag, gtk.keysyms.Q,
            gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)

        # add submenu
        self.submenuNew = gtk.Menu()

        for k, v in enumerate(self.actions['index']):
            if self.actions[v]['active']:
                label = self.actions[v]['label']
                item = gtk.MenuItem(label)
                self.submenuNew.append(item)
                item.connect('activate', self.on_subitem, k)
                item.show()

        self.itemNew.set_submenu(self.submenuNew)

    def manage_progressBar(self):
        ''' Manage progressbar '''

        task = self.up_progressBar()
        gobject.idle_add(task.next)

    def on_btnFile_clicked(self, widget):
        ''' When bouton File Chooser is clicked '''

        self.file_chooser()

    def on_btnGo_clicked(self, widget):
        ''' When bouton Go is clicked '''

        self.execute_hash()

    def on_btnQuit_clicked(self, widget):
        ''' When bouton Quit is clicked '''

        gtk.main_quit()

    def on_checkDirRecursive_toggled(self, widget):
        ''' When option recursive is choiced '''

        self.option_r = widget.get_active()

    def on_checksum_file_choosed(self, widget):
        ''' Get Files choosed '''

        self.fileChecksum = widget.get_filename()

    def on_click_statusIcon(self, widget):
        ''' When clic on status icon '''

        if self.mainWindow.get_property('visible'):
            self.mainWindow.hide()
        else:
            self.mainWindow.show()

    def on_comboAction_changed(self, widget):
        ''' When combobox action changed '''

        active = widget.get_active_text()

        for k, v in enumerate(self.actions['index']):
            if cmp(active, self.actions[v]['label']) == 0:
                self.action = v

        if self.action is not None:
            self.btnFile.set_sensitive(False)
            self.btnGo.set_sensitive(False)
            self.checkDirRecursive.set_sensitive(False)
            self.comboHash.set_active(-1)
            self.hbMainHash.set_sensitive(True)
            self.statusBar.push(0, str(active))
            self.vbFiler.set_sensitive(True)
            self.vbFile.set_sensitive(True)
            self.vbSum.set_sensitive(False)

        if self.action == 'controlByFile':
            self.btnFile.set_sensitive(True)
            self.hbMainHash.set_sensitive(False)

        self.labelFile.set_text(self.labels[self.action])

    def on_comboHash_changed(self, widget):
        ''' When combobox Hash changed '''

        algo = widget.get_active_text()

        for k, v in enumerate(self.algos['index']):
            if cmp(algo, self.algos[v]['label']) == 0:
                self.algo = v

        if self.algo is not None:
            self.btnFile.set_sensitive(True)
            self.vbFile.set_sensitive(True)

            if self.action == 'calculFolder':
                self.checkDirRecursive.set_sensitive(True)

            elif self.action == 'control':
                self.vbSum.set_sensitive(True)

            else:
                self.vbSum.set_sensitive(False)

    def on_itemAbout_activate(self, widget):
        ''' Call about window '''

        self.display_about_window()

    def on_itemNew_activate(self, widget):
        ''' Bypass '''

        pass

    def on_itemPref_activate(self, widget):
        ''' Call preferences window '''

        self.display_pref_window()

    def on_itemQuit_activate(self, widget):
        ''' Quit software '''

        gtk.main_quit()

    def on_mainWindow_destroy(self, widget):
        ''' Quit software '''
        self.log.info('=> Destroying Window Glade')
        gtk.main_quit()

    def on_menu_statusIcon(self, status_icon, button, activate_time):
        ''' Manage menu for the status icon '''

        self.menuSI = gtk.Menu()
        self.itemQuitSI = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.itemQuitSI.add_accelerator('activate', self.ag, gtk.keysyms.Q,
            gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        self.itemQuitSI.connect('activate', gtk.main_quit)
        self.menuSI.append(self.itemQuitSI)
        self.menuSI.popup(None, None, gtk.status_icon_position_menu, button,
            activate_time, status_icon)
        self.menuSI.show_all()

    def on_subitem(self, widget, index):
        ''' Get focus on combobox Action when menu is activated '''

        self.comboAction.grab_focus()

        self.action = index

        for k, v in enumerate(self.actions['index']):
            if k == index:
                self.comboAction.set_active(k)
                self.statusBar.push(0, self.actions[v]['label'])

    def on_txtSum_changed(self, widget):
        ''' When checksum is adding '''

        self.checksum = widget.get_text()

        if hasattr(self, 'checksum'):
            if self.checksum:
                self.btnGo.set_sensitive(True)
            else:
                self.btnGo.set_sensitive(False)

    def out_system(self):
        ''' Define variable out... for output file '''

        setattr(self, 'out',
                file(os.path.join(self.dir, self.dirs[0], 'out')).read())
        if self.out not in self.outs['index']:
            self.out = 'xml'

    def read_file_txt(self):
        ''' Read content file txt '''
        # Necessary that content eq 'ckecksum name_file'

        if self.file['ext'] in self.algos['index']:
            self.algo = self.file['ext']
            self.txt = dict()
            self.txt['checksum'] = dict()
            self.txt['name'] = dict()

            if os.path.exists(self.fileChecksum):
                try:
                    f = open(self.fileChecksum, 'r')
                    lines = f.readlines()
                    f.close()
                except:
                    self.log.exception('WG : You have a problem to read checksum file: %s!' % self.fileChecksum)
                    self.exit()

                if lines:
                    x = 0
                    for l in lines:
                        l = l.replace('\n', '')
                        self.txt['checksum'][x], self.txt['name'][x] = l.split(' ')
                        x += 1

                    self.log.debug('WG: Lines file cheksum are %s ' % self.txt)

    def read_file_xml(self):
        ''' Read content file xml , generated by this software! '''

        try :
            parser = XML_Parser()
            parser.set_debug(self.debug)
            parser.set_log(self.log)
            parser.read_xml(self.fileChecksum)

            self.xml = parser.get_dict_xml()

        except:
            self.log.warning('WG : You have a problem to read XML file: %s!' % self.fileChecksum)
            return False

    def re_init_all(self):
        ''' Re-initialize variables '''

        self.progressBar.set_text('')

        self.btnGo.set_sensitive(False)

        self.comboAction.set_active(-1)
        self.comboHash.set_active(-1)

        self.init_arrays()

        self.statusBar.push(0, '')

        self.txtSum.set_text('')

        self.vbFile.set_sensitive(False)
        self.vbSum.set_sensitive(False)

        self.checksum = None
        self.end = False

        self.flag = ''
        self.mssg = ''

    def run(self):
        ''' Launcher methodes '''
        # create gui
        self.create_gui()

        self.auto_connect_events()

        # manage main window
        self.create_status_icon()
        self.create_window()

        # manage menu
        self.manage_menu()

        # test python version
        if self.test_PyVersion():
            self.view_dialog_error()

        # else run-it!
        else:
            self.get_algorithms()

            self.view_dialog_main()

        if self.libgui == 'gtkbuilder':
            self.gui.connect_signals(self)

    def test_PyVersion(self):
        ''' Test python version '''

        b = False    # boolean
        m = 2.6        # minimum (version)

        if m > self.pyVersion :
            b = True

        return b

    def up_progressBar(self):
        ''' Manage progressbar '''

        #self.lock.acquire()
        self.progressBar.set_text('')
        count = 0.00

        while True:
            sleep(0.01)
            count += 0.1

            if count >= 0 and count <= 0.1:
                self.progressBar.set_text(self.text['progress_init'])

            elif count > 0.1 and count < 1:
                self.progressBar.set_text(self.text['progress_run'])

            elif count >= 1:
                self.progressBar.set_text(self.text['progress_end'])

                #self.lock.release()
                #return False

            self.progressBar.set_fraction(count / 1.0)
            yield True

        self.progressBar.set_text('')
        yield False

    def verify_algo_xml(self):
        ''' Verify if algo onto xml is good! '''

        self.algorithm = self.xml['algorithm']

        # if algo onto xml are not good
        if self.algorithm not in self.algos:
            self.flag = 'error'
            self.mssg = self.text['error_algo_xml']

            return False

        else:
            self.algo = self.algorithm

    def verify_txtSum_empty(self):
        ''' Boolean onto checksum '''

        if self.action == 'control' and not self.checksum:

            self.flag = 'warning'
            self.mssg = self.text['checksum_warn_empty']

            if self.txtSum.get_can_focus():
                self.txtSum.grab_focus()

            return False

        else:
            return True

    def view_dialog_error(self):
        ''' Display information error on dialog '''

        self.vboxError.set_visible(True)
        self.vboxMain.set_visible(False)

        self.labelError.set_text(self.text['error_version']) % self.pyVersion
        self.mainWindow.set_title(self.title['error_version'])

    def view_dialog_main(self):
        ''' Display information main on dialog '''

        self.vboxError.set_visible(False)
        self.vboxMain.set_visible(True)

        self.checkDirRecursive.set_sensitive(False)
        self.hbMainHash.set_sensitive(False)
        self.vbFiler.set_sensitive(False)
        self.vbSum.set_sensitive(False)
        self.btnGo.set_sensitive(False)

        self.labelHash.set_text(self.text['labelHash'])
        self.labelAction.set_text(self.text['labelAction'])
        self.labelFile.set_text(self.text['labelFile'])
        self.labelSum.set_text(self.text['labelSum'])

        self.comboAction = self.fill_combo(self.comboAction, self.actions)
        self.comboHash = self.fill_combo(self.comboHash, self.algos)

        self.checkDirRecursive.set_label(self.text['option_r'])


