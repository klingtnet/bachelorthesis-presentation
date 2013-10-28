#	Andreas Linz
#	admin@klingt.net
#	HTWK - 10INB-T
#
#	Makefile for thesis presentation

SHELL=/bin/bash
SCRIPT=build.py
PRESENTATION=content/presentation.tex
OPTS=--passes 2

all:
	@echo "building presentation ..."
	@python ${SCRIPT} ${PRESENTATION} ${OPTS}

clean:
	@echo "cleaning temporary files ..."
	ls -l .build
	rm --recursive --verbose --interactive=once .build

present:
	impressive --page-progress --supersample presentation.pdf
	# press t twice in the first page, to activate time tracking mode in terminal window!
