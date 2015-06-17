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

.PHONY:output_dir_set

output_dir_set:
OUTPUT_DIR =
ifneq "$(strip $(output_dir))" ""
OUTPUT_DIR = --output_dir=$(output_dir)
endif
FLGS += $(OUTPUT_DIR)
