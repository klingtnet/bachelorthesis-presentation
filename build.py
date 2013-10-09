#!/usr/bin/python3

"""
Build script for bachelor thesis presentation

Andreas Linz
admin@klingt.net
HTWK - 10INB-T
"""

import sys
import os
from shutil import copyfile
import argparse
from subprocess import check_call, call, Popen

debug = False
compiler = "xelatex"
build_dir = ".build"
passes = 1
path_to_texfile = ""
pdf = ""
texfile = ""
root_dir = ""

def main():
    # set commandline arguments and parse them
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="the texfile of your presentation")
    argparser.add_argument("--debug", help="enables debug output", action="store_true")
    argparser.add_argument("--passes", type=int, default=2, choices=range(1, 5), help="number of build passes")
    args = argparser.parse_args()   
    if args.debug:
        global debug
        debug = True
        print("debug output enabled!")
    if debug:
        print_debug("arguments: "+str(args))    
    if args.passes:
        global passes
        passes = args.passes
        print("Passes: {}").format(passes)

    # get directory of current script, used for copying output pdf
    global root_dir
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if debug:
        print_debug("script root: "+str(root_dir))

    # start the build script
    try:                
        with open(args.file):   # with automatically closes the file
            pass                               
    except IOError as e:
        print(e)
    else:
        process_filearg(args.file)
        start()

def start():
    if not check_dir(build_dir):
        if debug:
            print_debug(build_dir)
        os.mkdir(build_dir) 
    sync_build_dir()
    build_pdf()

def build_pdf():
    wd = [os.getcwd()] # working directory    
    wd.append(build_dir)
    wd.append(path_to_texfile)
    wd_str = "/".join(wd)        
    if debug:
        print_debug("working directory: "+str(wd_str))
    try:
        os.chdir(wd_str)
    except OSError as e:
        print(e)
    else:
        logfile_str = root_dir+"/"+"build.log"
        print("logfile: {}").format(logfile_str)
        try:
            with open(logfile_str, "w") as logfile:
                for i in range(passes):
                    print("build pass {} ...").format(i)
                    call(build_call(compiler, "-interaction=nonstopmode", texfile), stdout=logfile)
            copyfile(wd_str+"/"+pdf, root_dir+"/"+pdf)
        except IOError as e:
            print(e)

def sync_build_dir():
    """
    synchronizes the build directory with the content directory
    """
    source_dir = path_to_texfile
    dest_dir = build_dir
    return call(build_call("rsync", ["--archive", "--verbose"], source_dir, dest_dir)) 

def build_call(*args): # *.foo ellipsis
    """
    returns the arguments as flattened list
    """
    call = []    
    for arg in args:
        if type(arg) is list:
            for element in arg:
                call.append(element)        
        else:
            call.append(arg)
    if debug:
        print_debug("flattened call: "+str(call))
    return call

def check_dir(dir):
    return os.path.exists(dir)

def process_filearg(arg):
    pieces = arg.split("/")
    if debug:
        print_debug("splitted file argument: "+str(pieces))

    global texfile
    texfile = pieces.pop()
    global path_to_texfile
    path_to_texfile = "/".join(pieces)
    global pdf
    pdf = texfile.replace(".tex", ".pdf")

def print_debug(msg):
    print("DEBUG {}").format(msg)

if __name__ == "__main__":
    main()