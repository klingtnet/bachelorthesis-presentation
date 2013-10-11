#	Andreas Linz
#	admin@klingt.net
#	HTWK - 10INB-T
#
#	Makefile for thesis presentation

SHELL=/bin/bash
SCRIPT=build.py
TEXFILE=content/presentation.tex
OPTS=--passes 2 --debug

all:
	@echo "building presentation ..."
	@python ${SCRIPT} ${TEXFILE} ${OPTS} 

clean:
	@echo "cleaning temporary files ..."
	ls -l .build
	rm --recursive --verbose --interactive=once .build
