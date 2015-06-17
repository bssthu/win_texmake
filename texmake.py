#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : texmake.py
# Author        : bss
# Project       : win_texmake
# Creation Date : 2015-06-17
# Description   : 
# 

import os
from win32com.client.dynamic import Dispatch

if __name__ == '__main__':
    src = os.path.abspath('test.pdf')

    app = Dispatch('AcroExch.App')
    avdoc = Dispatch('AcroExch.AVDoc')

    avdoc.Open(src, src);
    avdoc.Close(-1);

    avdoc.Open(src, src);

    app.Show();

    pddoc = avdoc.GetPDDoc()
    pageNum = pddoc.GetNumPages()

    page = 10
    page = min(page, pageNum)

    pageview = avdoc.GetAVPageView()
    pageview.Goto(page)
