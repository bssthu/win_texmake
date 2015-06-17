# -*- coding: utf-8 -*-
# Platform: Windows
# Project: texmake
# created by bss at 2015-06-17

PYTHON = python
CD = cd


.PHONY:all

all:
	$(PYTHON) texmake.py

.PHONY:tex

tex:
	$(LATEX) 
