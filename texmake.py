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
import getopt
from win32com.client.dynamic import Dispatch
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def loadSetting(filename):
    cf = configparser.ConfigParser()
    cf.read(filename)

    texfile = cf.get('tex', 'texfile')
    working_dir = cf.get('tex', 'working_directory')
    output_dir = cf.get('tex', 'output_directory')

    LATEX = cf.get('cmd', 'LATEX')

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
    if (output_dir == None or output_dir == ''):
        output_dir = '.'

    return (texfile, working_dir, output_dir, LATEX)


def getOpts(argv):
    output_dir = ''
    try:
        opts, argv = getopt.getopt(argv[1:], '', ['output-directory='])
    except (Exception, e):
        print('unexcepted error when parse argv: %s' % e)
        return output_dir

    for o, a in opts:
        if o in ('--output-directory'):
            output_dir = a

    return output_dir


def callMake(texfile, project, working_dir, output_dir, LATEX):
    os.chdir(working_dir)
    cmd = '%s -file-line-error -output-directory=%s -halt-on-error %s' % (LATEX, output_dir, texfile)
    return os.system(cmd)


def getAVStatus(avdoc):
    pageview = avdoc.GetAVPageView()
    page = pageview.GetPageNum()
    zoomtype = pageview.GetZoomType()
    zoom = pageview.GetZoom()
    frame = avdoc.GetFrame()
    viewmode = avdoc.GetViewMode()
    return (page, zoomtype, zoom, frame, viewmode)


if __name__ == '__main__':
    # init
    (texfile, working_dir, output_dir, LATEX) = loadSetting('texmake.ini')
    output_dir_opt = getOpts(sys.argv)

    if output_dir_opt != '':
        output_dir = output_dir_opt
    project = texfile.split('.tex')[0]
    pdf_src = os.path.abspath('%s%s%s.pdf' % (output_dir, os.sep, project))
    pdf_src = os.path.abspath(pdf_src)

    app = Dispatch('AcroExch.App')
    avdoc = Dispatch('AcroExch.AVDoc')

    # get pageview status
    fileexists = os.path.isfile(pdf_src) and avdoc.Open(pdf_src, pdf_src)
    if fileexists:
        (page, zoomtype, zoom, frame, viewmode) = getAVStatus(avdoc)
        avdoc.Close(-1)
    if app.GetNumAVDocs() <= 0:
        app.Hide()

    # make
    code = callMake(texfile, project, working_dir, output_dir, LATEX)
    if code != 0:
        sys.exit(code)

    # open pdf
    if ((not os.path.isfile(pdf_src)) or (not avdoc.Open(pdf_src, pdf_src))):
        print('cannot open pdf, bye.')
        sys.exit(-1)

    # set page view
    if fileexists:
        avdoc.SetFrame(frame)
        avdoc.SetViewMode(viewmode)
        pddoc = avdoc.GetPDDoc()
        numPages = pddoc.GetNumPages()
        page = min(page, numPages)

        pageview = avdoc.GetAVPageView()
        pageview.Goto(page)
        pageview.ZoomTo(zoomtype, zoom)
    app.Show()

    app.Exit()
