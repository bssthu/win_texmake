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
    working_dir = cf.get('tex', 'working_dir')
    output_dir = cf.get('tex', 'output_dir')

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


def callMake(texfile, project, working_dir, output_dir, LATEX):
    os.chdir(working_dir)
    cmd = '%s %s -output-directory=%s -halt-on-error' % (LATEX, texfile, output_dir)
    os.system(cmd)


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
    callMake(texfile, project, working_dir, output_dir, LATEX)

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
