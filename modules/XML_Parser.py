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

import os
import sys
import xml.dom.minidom

from xml.dom.minidom import Document
from xml.dom.minidom import Node
from xml.dom.minidom import parse

class XML_Parser:

    def __init__(self):

        self.charset = sys.getdefaultencoding()

    def init_vars(self):

        for d in self.dic:
            setattr(self, d, self.dic[d])

            self.log.debug('XML Parser: Create variable self.%s needed...' % d)

    def build_xml(self):

        self.init_vars()

        self.doc = Document()

        self.root = self.doc.createElement('info')
        self.doc.appendChild(self.root)

        # create root attributes
        if hasattr(self, 'id'):
            self.root.setAttribute('id', self.id)

        # create child algo
        if hasattr(self, 'algorithm'):
            self.create_node_child('algorithm', self.root, self.algorithm)

        # create child generator
        if hasattr(self, 'generator'):
            self.create_node_child('generator', self.root, self.generator)

        # create childs files
        if hasattr(self, 'files'):
            self.build_array_for_node()

        self.xml = self.doc.toprettyxml(indent = '    ',
            encoding = self.charset)    # pour créer le fichier

    def build_array_for_node(self):

        if 'shortpath' in self.files and self.files['shortpath']:
            array = self.files['shortpath']

        elif 'base' in self.files and self.files['base']:
            array = self.files['base']

        for k, v in array.items():
            child = self.doc.createElement('file')
            self.root.appendChild(child)
            self.create_node_child('name', child, v)
            self.create_node_child('checksum', child, self.files['checksum'][k])
            self.create_node_child('size', child, str(self.files['size'][k]))
            self.create_node_child('date', child, str(self.files['date'][k]))

        del(array)

    def create_node_child(self, element, parent, text):
        child = self.doc.createElement(element)
        parent.appendChild(child)
        txt = self.doc.createTextNode(text.strip())
        child.appendChild(txt)

        # create child attribute
        if element == 'generator' and hasattr(self, 'version'):
            child.setAttribute('version', self.version.strip())


    def get_dict_xml(self):
        if hasattr(self, 'xml'):
            return self.xml
        else:
            return False

    def read_xml(self, doc):

        # comment verifier si fichier XML ?
        if os.path.exists(doc) and os.path.isfile(doc) :

            self.doc = xml.dom.minidom.parse(doc)

            self.xml = dict()

            infos = ['algorithm', 'generator', 'id', 'version']

            for info in infos:
                if info == 'id':
                    self.xml[info] = self.doc.getElementsByTagName('info')[0].getAttribute(info).encode(self.charset)
                elif info == 'version':
                    self.xml[info] = self.doc.getElementsByTagName('generator')[0].getAttribute(info).encode(self.charset)
                else:
                    self.xml[info] = self.doc.getElementsByTagName(info)[0].firstChild.nodeValue.encode(self.charset)

            entries = ['checksum', 'date', 'name', 'size']

            for entry in entries:
                self.xml[entry] = dict()

            x = 0
            for node in self.doc.getElementsByTagName('file'):
                for entry in entries:
                    if entry == 'size':
                        value = int(node.getElementsByTagName(entry)[0].firstChild.nodeValue.encode(self.charset))
                    else:
                        value = str(node.getElementsByTagName(entry)[0].firstChild.nodeValue.encode(self.charset))

                    self.xml[entry][x] = value

                x += 1

            self.log.debug('XML File: %s' % self.xml)

    def save_xml(self, filename):
        try:
            f = open(filename, 'w')
            f.write(self.xml)
            f.close()

        except IOError as ioe:
            self.log.exception('Error to create document XML: %s' % ioe)
            return False

    def set_debug(self, entry):
        self.debug = bool(entry)

    def set_dict(self, entry):
        self.dic = dict(entry)

    def set_log(self, entry):
        self.log = entry

