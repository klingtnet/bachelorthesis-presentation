#!/usr/bin/python3

"""Build script for bachelor thesis presentation

Andreas Linz
admin@klingt.net
HTWK - 10INB-T
"""

import sys
import os
import argparse
from subprocess import check_call, call

debug = False
compiler = "xelatex"
build_dir = ".build/"
texfile = ""

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="the texfile of your presentation")
    argparser.add_argument("--debug", help="enables debug output", action="store_true")
    args = argparser.parse_args()    
    if args.debug:
        global debug
        debug = True
        print("debug output enabled!")
    if debug:
        print("DEBUG: {}").format(args)    
    try:        
        # with automatically closes the file
        with open(args.file):
            global texfile
            texfile = args.file                           
        build()                                
    except IOError as ex:
        print(ex)
    pass

def build():
    if not check_dir(build_dir):
        if debug:
            print("DEBUG: creating build directory {}").format(build_dir)
        os.mkdir(build_dir) 
    sync_build_dir()
    build_pdf()

def build_pdf():
    #return call(build_call(compiler, "-halt-on-error", build_dir+texfile))
    pass

def sync_build_dir():
    source_dir = "content"
    dest_dir = build_dir
    return call(build_call("rsync", ["--archive", "--verbose"], source_dir, dest_dir)) 

def build_call(*args): # *.foo ellipsis
    call = []    
    for arg in args:
        if type(arg) is list:
            for element in arg:
                call.append(element)        
        else:
            call.append(arg)
    if debug:
        print("DEBUG: {}").format(call)
    return call

def check_dir(dir):
    return os.path.exists(dir)

if __name__ == "__main__":
    main()