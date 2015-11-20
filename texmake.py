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
    bibfile = cf.get('tex', 'bibfile')
    working_dir = cf.get('tex', 'working_directory')
    output_dir = cf.get('tex', 'output_directory')

    LATEX = cf.get('cmd', 'LATEX')
    BIBTEX = cf.get('cmd', 'BIBTEX')

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
    if (bibfile == None or bibfile == ''):
        bibfiles = []
        for file in os.listdir(working_dir):
            if file.endswith('.bib'):
                bibfiles.append(file)
        if len(bibfiles) == 1:
            bibfile = bibfiles[0]
        else:
            bibfile = ''    # ignore
    if (output_dir == None or output_dir == ''):
        output_dir = '.'

    return (texfile, bibfile, working_dir, output_dir, LATEX, BIBTEX)


def getOpts(argv):
    output_dir = ''
    bib = False
    try:
        opts, argv = getopt.getopt(argv[1:], '', ['output-directory=','bib'])
    except (Exception, e):
        print('unexcepted error when parse argv: %s' % e)
        return output_dir

    for o, a in opts:
        if o in ('--output-directory'):
            output_dir = a
        if o in ('--bib'):
            bib = True

    return (output_dir, bib)


def callMake(texfile, bibfile, project, working_dir, output_dir, bib, LATEX, BIBTEX):
    working_dir = os.path.abspath(working_dir)
    os.chdir(working_dir)
    if bib and bibfile != '':
        cmd = 'cp %s %s%s%s' % (bibfile, output_dir, os.sep, bibfile)
        os.system(cmd)

    # make first pass
    cmd_tex = '%s -file-line-error -output-directory=%s -halt-on-error %s' % (LATEX, output_dir, texfile)
    code = os.system(cmd_tex)
    if code != 0:
        return code

    if bib and bibfile != '':
        # if bib, make bib
        os.chdir(output_dir)
        cmd_bib = '%s %s' % (BIBTEX, bibfile[:-4])
        code = os.system(cmd_bib)
        if code != 0:
            return code

        os.chdir(working_dir)
        # if bib, make second pass
        code = os.system(cmd_tex)
        if code != 0:
            return code
        # if bib, make third pass
        code = os.system(cmd_tex)
        if code != 0:
            return code

    return code


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
    (texfile, bibfile, working_dir, output_dir, LATEX, BIBTEX) = loadSetting('texmake.ini')
    (output_dir_opt, bib_opt) = getOpts(sys.argv)

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
    code = callMake(texfile, bibfile, project, working_dir, output_dir, bib_opt, LATEX, BIBTEX)
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
