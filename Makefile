# -*- coding: utf-8 -*-
# Platform: Windows
# Project: texmake
# created by bss at 2015-06-17

PYTHON = python
CD = cd
FLGS =


.PHONY:all

all:
	$(PYTHON) texmake.py $(FLGS)

.PHONY:bib

bib:
	$(PYTHON) texmake.py $(FLGS) --bib

.PHONY:output_dir_set

output_dir_set:
OUTPUT_DIR =
ifneq "$(strip $(output-directory))" ""
OUTPUT_DIR = --output-directory=$(output-directory)
endif
FLGS += $(OUTPUT_DIR)
