#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : texmake.py
# Author        : bss
# Project       : win_texmake
# Creation Date : 2015-06-17
# Description   : https://github.com/bssthu/win_texmake
# 

import sys
import os
from win32com.client.dynamic import Dispatch
import ConfigParser


def loadSetting(filename):
    cf = ConfigParser.ConfigParser()
    cf.read(filename)

    texfile = cf.get('tex', 'texfile')
    project = cf.get('tex', 'project')
    working_dir = cf.get('tex', 'working_dir')
    output_dir = cf.get('tex', 'output_dir')
    
    if (working_dir == None or working_dir == ''):
        working_dir = '.'
    if (texfile == None or texfile == ''):
        texfiles = []
        for file in os.listdir(working_dir):
            if file.endswith('.tex'):
                texfiles.append(file)
        if len(texfiles) == 1:
            texfile = texfiles[0]
        else:
            print('cannot decide texfile, please edit texmake.ini')
            sys.exit(-1)
    if (project == None or project == ''):
        project = texfile.split('.tex')[0]
    if (output_dir == None or output_dir == ''):
        output_dir = '.'

    return (texfile, project, working_dir, output_dir)


def getPageAndZoom(avdoc):
    pageview = avdoc.GetAVPageView()
    page = pageview.GetPageNum()
    zoom = pageview.GetZoom()
    return (page, zoom)


if __name__ == '__main__':
    # init
    (texfile, project, working_dir, output_dir) = loadSetting('texmake.ini')
    pdf_src = os.path.abspath('%s%s%s.pdf' % (output_dir, os.sep, project))
    pdf_src = os.path.abspath(pdf_src)

    app = Dispatch('AcroExch.App')
    avdoc = Dispatch('AcroExch.AVDoc')

    # get pageview status
    if not avdoc.Open(pdf_src, pdf_src):
        print('cannot open pdf, bye.')
        sys.exit(0)
    (page, zoom) = getPageAndZoom(avdoc)
    avdoc.Close(-1)

    # open pdf
    if not avdoc.Open(pdf_src, pdf_src):
        print('cannot open pdf, bye.')
        sys.exit(0)
    app.Show();

    pddoc = avdoc.GetPDDoc()
    numPages = pddoc.GetNumPages()
    page = min(page, numPages)

    pageview = avdoc.GetAVPageView()
    pageview.Goto(page)
