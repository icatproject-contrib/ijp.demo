#!/usr/bin/env python

# Test batch job arguments
# Essentially, just reports whatever it finds on the command line
# usage: test_args options
# (mandatory) options: --sessionId=<sessionId> --icatUrl=<icatUrl> --idsUrl=<idsUrl>
# optional options: --datasetIds=<id1,...> --datafileIds=<id1,...> (though normally at least one would be defined)
# Further options: --option1=<string> --option2=<string>

import sys
import os
import logging

# Use local cat_utils.py - a proper installation would install it as a package
from cat_utils import IjpOptionParser

logging.basicConfig(level=logging.CRITICAL)

usage = "usage: %prog options"

parser = IjpOptionParser(usage)

# Options specific to this script
# Job Type specs can choose to use these, but can't invent their own
# (parse_args() will throw an error for unknown options)
# NOTE: most options specified here only have a long-form,
# so must always appear on the command-line as --option-name=value or --option-name value,
# even for boolean flags. '--silent --viewtype blah' will set 'silent' to '--viewtype',
# and leave 'blah' as an argument instead of as the value of the viewtype option.

parser.add_option("--option-one", dest="optionOne",
                 help="script-specific option 1")
parser.add_option("--option-two", dest="optionTwo",
                 help="script-specific option 2")
parser.add_option("--mode", dest="mode",
                  help="plain, verbose or effusive")
parser.add_option("--silent", dest="silent",
                  help="keep quiet, regardless of --mode")
parser.add_option("--viewtype", dest="viewtype",
                  help="View type (fullframe, beads, etc.)")
parser.add_option("--index", dest="index",
                  help="Initial index (0-10, default 1)")
parser.add_option("--origin", dest="origin",
                  help="Origin (range [-2.0,2.0]")

(options, args) = parser.parse_args()

jobName = os.path.basename(sys.argv[0])
print jobName, "starting..."

rest = args  

if options.sessionId:
    print "ICAT sessionId provided"
else:
    print "No ICAT sessionId provided"

# Report icat/ids URLs if present

if options.icatUrl:
    print "ICAT url =", options.icatUrl
else:
    print "ICAT url not supplied"

if options.idsUrl:
    print "IDS url =", options.idsUrl
else:
    print "IDS url not supplied"

if options.datasetIds:
    print "datasetIds = ", options.datasetIds
else:
    print "datasetIds not supplied"

if options.datafileIds:
    print "datafileIds = ", options.datafileIds
else:
    print "datafileIds not supplied"

if options.optionOne:
    print "Option 1 = ", options.optionOne

if options.optionTwo:
    print "Option 2 = ", options.optionTwo

if options.mode:
    print "Mode = ", options.mode

if options.silent:
    # Note: print the value of silent; we expect a boolean,
    # but this helps debug misuses such as 'test_args --silent --viewtype whitebeam'
    print "Silent = ", options.silent
else:
    print "Silent = false"
    
if options.viewtype:
    print "View type = ", options.viewtype
    
if options.index:
    print "Index = ", options.index

if options.origin:
    print "Origin = ", options.origin

print "Other command-line arguments (if any): ", args

print jobName, "completed."
